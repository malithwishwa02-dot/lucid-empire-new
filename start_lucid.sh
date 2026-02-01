#!/bin/bash
echo "[*] LUCID EMPIRE INITIALIZATION..."

# TASK C: Shield Activation
echo "[*] Activating Network Shield (XDP)..."
if [ -f "./network/xdp_loader.sh" ]; then
    chmod +x ./network/xdp_loader.sh
    ./network/xdp_loader.sh load
else
    echo "[!] Network Shield Loader not found."
fi

echo "[*] Installing GUI Dependencies..."
pip3 install tk --quiet
echo "[*] Launching Commander..."
python3 lucid_manager.py
