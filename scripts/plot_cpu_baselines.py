import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("plots").mkdir(exist_ok=True)

aes = pd.read_csv("data/raw/cpu_aes_ctr.csv")
sha = pd.read_csv("data/raw/cpu_sha.csv")

# Load OpenSSL results if present
evp_path = Path("data/raw/openssl_evp.csv")
evp = pd.read_csv(evp_path) if evp_path.exists() else None

# AES-CTR throughput vs size
plt.figure()
x = aes["size_bytes"].values
y = aes["throughput_Bps"].values / 1e9
plt.plot(x, y, marker="o", label="AES-CTR (CPU)")

# OpenSSL AES overlay
if evp is not None and "aes-128-ctr" in evp["algo"].unique():
    sub = evp[evp["algo"] == "aes-128-ctr"].sort_values("size_bytes")
    plt.plot(sub["size_bytes"], sub["throughput_Bps"]/1e9,
             marker="x", linestyle="--", label="OpenSSL AES-128-CTR")
    

plt.xscale("log", base=2)
plt.xlabel("Message size (bytes)")
plt.ylabel("Throughput (GB/s)")
plt.title("CPU Throughput: AES-CTR")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("plots/cpu_aes_ctr.png")

# SHA throughput vs size
plt.figure()
for algo in sha["algo"].unique():
    sub = sha[sha["algo"] == algo]
    plt.plot(sub["size_bytes"], sub["throughput_Bps"]/1e9, marker="o", label=algo)
    
# OpenSSL SHA overlays
if evp is not None:
    for a, label in [("sha256","OpenSSL SHA-256"), ("sha512","OpenSSL SHA-512")]:
        if a in evp["algo"].unique():
            sub = evp[evp["algo"] == a].sort_values("size_bytes")
            plt.plot(sub["size_bytes"], sub["throughput_Bps"]/1e9,
                     marker="x", linestyle="--", label=label)

plt.xscale("log", base=2)
plt.xlabel("Message size (bytes)")
plt.ylabel("Throughput (GB/s)")
plt.title("CPU Throughput: SHA-256/512")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("plots/cpu_sha.png")

print("Wrote plots to plots/")
