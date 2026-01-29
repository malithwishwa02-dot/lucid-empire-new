#!/bin/bash
# LUCID EMPIRE :: LAUNCH PROTOCOL v5.0
# AUTHORITY: Dva.12
# FUNCTION: Privilege Escalation & Python Handoff

PROFILE_ID=$1

echo "=================================================="
echo "   LUCID EMPIRE :: LAUNCH SEQUENCE INITIATED"
echo "   TARGET PROFILE: $PROFILE_ID"
echo "=================================================="

if [ -z "$PROFILE_ID" ]; then
    echo "[!] ERROR: No Profile ID received from Commander."
    echo "    USAGE: ./start_lucid.sh <UUID>"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "[!] AUTHORITY: User is not ROOT."
    echo "[*] ESCALATION: Requesting sudo privileges for Kernel Injection..."
    exec sudo "$0" "$PROFILE_ID"
    exit
fi

echo "[*] STATUS: ROOT ACCESS GRANTED."
echo "[*] CORE: Initializing Docker Interface..."
echo "[*] NET:  Loading XDP Packet Mask (Windows 10 Signature)..."

if [ -f "lucid_launcher.py" ]; then
    python3 lucid_launcher.py --launch "$PROFILE_ID" --mode manual
else
    echo "[!] CRITICAL: lucid_launcher.py not found in current directory."
    echo "    PATH: $(pwd)"
    exit 1
fi

echo "[*] SESSION TERMINATED."
