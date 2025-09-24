from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os, time, csv, pathlib

# Measures the throughput of AES-CTR on the CPU across different message sizes
# Pick a size (1 KiB, 16 KiB, 1 MiB, 16 MiB) and run each for ITERS
# Generate a random key and 8-byte nonce, create a cypher, and repeatedly encrypt over the buffer
# Then calculate throughput (size * ITERS) / elapsed time in bytes per second
# Repeat this for each size, then log in the csv under cols algo, mode, key_bits, size_bytes, throughput_Bps

# Throughput should generally increase with larger buffers (less overhead per byte).

SIZES = [1024, 16384, 1<<20, 1<<24]  # 1 KiB, 16 KiB, 1 MiB, 16 MiB
ITERS = 32

def bench(size, key_bits=128):
    key   = get_random_bytes(key_bits//8)
    nonce = get_random_bytes(8)  # CTR: nonce_len + counter_len == 16
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    buf = os.urandom(size)
    cipher.encrypt(buf)  # warmup
    t0 = time.perf_counter()
    for _ in range(ITERS):
        cipher.encrypt(buf)
    t1 = time.perf_counter()
    return (size * ITERS) / (t1 - t0)  # bytes/sec

def main():
    outp = pathlib.Path("data/raw/cpu_aes_ctr.csv")
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["algo","mode","key_bits","size_bytes","throughput_Bps"])
        w.writeheader()
        for sz in SIZES:
            thr = bench(sz, 128)
            w.writerow({"algo":"AES","mode":"CTR","key_bits":128,"size_bytes":sz,"throughput_Bps":thr})
    print(f"Wrote {outp}")

if __name__ == "__main__":
    main()
