#!/usr/bin/env bash
set -euo pipefail
out="data/sysinfo/$(hostname)_sysinfo.txt"
mkdir -p "$(dirname "$out")"
{
  date -Is
  echo "---- uname -a ----"; uname -a
  echo "---- lscpu ----"; lscpu
  echo "---- meminfo ----"; head -n 25 /proc/meminfo
  echo "---- OpenSSL ----"; openssl version -a || true
  echo "---- Python ----"; python3 --version
} > "$out"
echo "Wrote $out"
