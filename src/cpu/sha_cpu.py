import hashlib, os, time, csv, pathlib

# Measure throughput for SHA256 and SHA512 on the CPU by message size
# For each size and algorithm:
# - Create a random buffer
# - Warm-up with one digest
# - Time in the loop: create a new hash object, update with the full buffer, call .digest()
# Then compute throughput in bytes/sec

# SHA-512 is typically expected to run 

SIZES = [1024, 16384, 1<<20, 1<<24]
ITERS = 64

def bench(alg, size):
    buf = os.urandom(size)
    getattr(hashlib, alg)(buf).digest()  # warmup
    t0 = time.perf_counter()
    for _ in range(ITERS):
        h = getattr(hashlib, alg)()
        h.update(buf)
        _ = h.digest()
    t1 = time.perf_counter()
    return (size * ITERS) / (t1 - t0)  # bytes/sec

def main():
    outp = pathlib.Path("data/raw/cpu_sha.csv")
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["algo","size_bytes","throughput_Bps"])
        w.writeheader()
        for alg in ["sha256","sha512"]:
            for sz in SIZES:
                thr = bench(alg, sz)
                w.writerow({"algo":alg.upper(),"size_bytes":sz,"throughput_Bps":thr})
    print(f"Wrote {outp}")

if __name__ == "__main__":
    main()
