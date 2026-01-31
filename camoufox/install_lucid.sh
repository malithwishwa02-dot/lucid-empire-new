#!/bin/bash

# LUCID EMPIRE :: AUTOMATED DEPLOYMENT PROTOCOL
# AUTHORITY: PROMETHEUS-CORE
# PLATFORM: LINUX (Debian/Ubuntu)

echo "=================================================="
echo "   LUCID EMPIRE :: INITIALIZING DEPLOYMENT        "
echo "=================================================="

# 1. ELEVATION CHECK
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run as root (sudo ./install_lucid.sh)"
  exit
fi

# 2. SYSTEM DEPENDENCIES
echo "[*] INSTALLING CORE DEPENDENCIES..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-tk clang llvm libelf-dev gcc-multilib docker.io docker-compose

# 3. PYTHON ENVIRONMENT
echo "[*] INSTALLING PYTHON LIBRARIES..."
pip3 install requests playwright termcolor
playwright install deps

# 4. FONT HARMONIZATION (Preventing Linux Leak)
echo "[*] HARMONIZING FONTS (Microsoft Core)..."
echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
apt-get install -y ttf-mscorefonts-installer fonts-liberation2
fc-cache -f -v

# 5. NETWORK MASK COMPILATION (eBPF)
echo "[*] COMPILING NETWORK MASK (XDP)..."
if [ -f "lucid empire/network/xdp_outbound.c" ]; then
    clang -O2 -target bpf -c "lucid empire/network/xdp_outbound.c" -o "lucid empire/network/xdp_outbound.o"
    echo "    [SUCCESS] Kernel Object Compiled."
else
    echo "    [ERROR] xdp_outbound.c not found!"
fi

# 6. PERMISSIONS
echo "[*] SETTING PERMISSIONS..."
chmod +x "lucid empire/start_lucid.sh"
chmod +x "lucid empire/lucid_launcher.py"
chmod +x "lucid empire/lucid_manager.py"

# 7. BINARY CHECK (Placeholder)
if [ ! -f "lucid empire/bin/firefox/firefox" ]; then
    echo "[!] WARNING: Compiled Binary missing in ./bin/firefox/"
    echo "    Run the GitHub Workflow to generate the warhead."
fi

echo "=================================================="
echo "   DEPLOYMENT COMPLETE.                           "
echo "   RUN: ./lucid\ empire/start_lucid.sh            "
echo "=================================================="
