#!/usr/bin/env python3
# Runs: openssl speed -elapsed -bytes <size> -evp <algo>
# Writes: data/raw/openssl_evp.csv  (algo,size_bytes,throughput_Bps,openssl_version,ts)

import argparse, csv, datetime as dt, re, subprocess
from pathlib import Path

DEFAULT_ALGOS = ["sha256", "sha512", "aes-128-ctr"]
DEFAULT_SIZES = [1024, 16384, 1<<20, 1<<24]  # 1 KiB, 16 KiB, 1 MiB, 16 MiB

def run(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{p.stderr}")
    return p.stdout

def openssl_version() -> str:
    try: return run("openssl version").strip()
    except: return "unknown"

def parse_throughput_k_or_m(text: str, label: str) -> float:
    """
    Parse a line like: 'sha256  123456.78k' → bytes/sec
    We search only the tail of output to avoid banners.
    """
    tail = "\n".join(text.splitlines()[-40:])
    m = re.search(rf"^\s*{re.escape(label)}\s+([0-9]+(?:\.[0-9]+)?)([kKmM]?)",
                  tail, flags=re.MULTILINE)
    if not m:
        raise ValueError(f"Couldn't parse throughput for {label}.\nOutput tail:\n{tail}")
    val = float(m.group(1))
    suf = m.group(2).lower()
    if suf == "k": val *= 1_000.0
    elif suf == "m": val *= 1_000_000.0
    return val  # bytes/sec

def bench(algo: str, size: int, seconds: int) -> float:
    out = run(f"openssl speed -elapsed -seconds {seconds} -bytes {size} -evp {algo}")
    return parse_throughput_k_or_m(out, algo)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--algos", nargs="*", default=DEFAULT_ALGOS)
    ap.add_argument("--sizes", nargs="*", type=int, default=DEFAULT_SIZES)
    ap.add_argument("--seconds", type=int, default=3)
    ap.add_argument("--out", default="data/raw/openssl_evp.csv")
    args = ap.parse_args()

    Path("data/raw").mkdir(parents=True, exist_ok=True)
    ver = openssl_version()
    ts  = int(dt.datetime.utcnow().timestamp())

    rows = []
    for algo in args.algos:
        for sz in args.sizes:
            try:
                bps = bench(algo, sz, args.seconds)
                rows.append({"algo": algo, "size_bytes": sz,
                             "throughput_Bps": bps,
                             "openssl_version": ver, "ts": ts})
                print(f"{algo:12} size={sz:8} -> {bps/1e9:.3f} GB/s")
            except Exception as e:
                print(f"[WARN] {algo} size={sz}: {e}")

    if rows:
        with open(args.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["algo","size_bytes","throughput_Bps","openssl_version","ts"])
            w.writeheader(); w.writerows(rows)
        print(f"Wrote {args.out} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
