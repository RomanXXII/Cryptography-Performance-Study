General notes:
CPU Results
- Repeated testing suggested that SHA-256 yielded significantly higher throughput than SHA-512, contrary to what is typically expected. Cross-checking via openssl speed sha256 and openssl speed 512 confirmed similar results. This is likely due to the x86 extensions (sha_ni) available for SHA-256 but not SHA-512.