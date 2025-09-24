#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/sysinfo
{
  date -Is
  echo "---- uname -a ----"; uname -a
  echo "---- lscpu ----"; lscpu
  echo "---- /proc/meminfo ----"; head -n 25 /proc/meminfo
  echo "---- OpenSSL ----"; openssl version -a
} > data/sysinfo/$(hostname)_sysinfo.txt
echo "Wrote data/sysinfo/$(hostname)_sysinfo.txt"
