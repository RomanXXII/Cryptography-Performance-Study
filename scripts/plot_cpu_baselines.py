import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("plots").mkdir(exist_ok=True)

aes = pd.read_csv("data/raw/cpu_aes_ctr.csv")
sha = pd.read_csv("data/raw/cpu_sha.csv")

# AES-CTR throughput vs size
plt.figure()
x = aes["size_bytes"].values
y = aes["throughput_Bps"].values / 1e9
plt.plot(x, y, marker="o", label="AES-CTR (CPU)")
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
plt.xscale("log", base=2)
plt.xlabel("Message size (bytes)")
plt.ylabel("Throughput (GB/s)")
plt.title("CPU Throughput: SHA-256/512")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("plots/cpu_sha.png")

print("Wrote plots to plots/")
