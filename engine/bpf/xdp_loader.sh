#!/bin/bash
# OBLIVION NETWORK LOADER (XDP)
# Usage: ./xdp_loader.sh [load|unload] [interface]
# Requires: iproute2, clang

ACTION=$1
IFACE=$2
OBJ_FILE="./network/xdp_outbound.o"

if [ -z "$IFACE" ]; then
    # Auto-detect default interface
    IFACE=$(ip route | grep default | sed -e 's/^.*dev.//' -e 's/.proto.*//')
fi

echo "[*] Target Interface: $IFACE"

if [ "$ACTION" == "load" ]; then
    if [ ! -f "$OBJ_FILE" ]; then
        echo "[!] Binary object $OBJ_FILE not found. Run audit_and_fix.py first."
        exit 1
    fi
    echo "[+] Loading XDP Shield on $IFACE..."
    # Force generic mode if native driver support is missing
    sudo ip link set dev $IFACE xdpobj $OBJ_FILE sec .text || sudo ip link set dev $IFACE xdpgeneric obj $OBJ_FILE sec .text
    echo "[+] Shield Active. OS Fingerprints masked."

elif [ "$ACTION" == "unload" ]; then
    echo "[-] Unloading XDP Shield..."
    sudo ip link set dev $IFACE xdp off
    echo "[-] Shield Deactivated."

else
    echo "Usage: $0 [load|unload] <interface>"
    exit 1
fi
