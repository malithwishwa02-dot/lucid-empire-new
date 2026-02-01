#!/bin/bash
# XDP Program Loader Script
# Loads eBPF/XDP program on specified network interface

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <interface> <xdp_program.o>"
    exit 1
fi

INTERFACE="$1"
PROGRAM="$2"

echo "[*] Loading XDP program on $INTERFACE..."
echo "[*] Program: $PROGRAM"

if [ ! -f "$PROGRAM" ]; then
    echo "[!] Program file not found: $PROGRAM"
    exit 1
fi

echo "[+] Compiling and loading XDP program..."
ip link set dev "$INTERFACE" xdp obj "$PROGRAM"

echo "[+] XDP program loaded successfully"
echo "[*] Verifying load..."
ip link show dev "$INTERFACE" | grep xdp

echo "[+] Ready for operation"
