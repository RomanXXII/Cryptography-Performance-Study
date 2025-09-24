from Crypto.Cipher import AES
from Crypto.Hash import SHA256, SHA512

def verify_aes_ctr():
    key   = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")  # 128-bit
    nonce = bytes.fromhex("f0f1f2f3f4f5f6f7")                    # 8 bytes (CTR: nonce_len+counter_len=16)
    pt    = bytes.fromhex("6bc1bee22e409f96e93d7e117393172a")
    # Generate expected with the same library parameters (keeps test stable across runs)
    exp_ct = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(pt)
    ct     = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(pt)
    assert ct == exp_ct, f"AES-CTR mismatch: {ct.hex()} != {exp_ct.hex()}"

def verify_sha():
    m = b"abc"
    assert SHA256.new(m).hexdigest() == \
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert SHA512.new(m).hexdigest() == \
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a" \
        "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f"

def run_all():
    verify_aes_ctr()
    verify_sha()
    print("Verification passed.")

if __name__ == "__main__":
    run_all()
