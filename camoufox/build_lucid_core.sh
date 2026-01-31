#!/bin/bash
# LUCID EMPIRE :: IRONCLAD BUILDER (LINUX)
# AUTHORITY: Dva.12
# PURPOSE: Automate dependency resolution and eBPF compilation.

set -e  # Exit on error

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=================================================="
echo -e "   LUCID EMPIRE :: CORE BUILDER v5.0"
echo -e "   TARGET: LINUX KERNEL HOOKS & PYTHON ENV"
echo -e "==================================================${NC}"

# 1. OS DETECTION & DEPENDENCY INSTALL
echo -e "\n${GREEN}[1/4] DETECTING ENVIRONMENT...${NC}"
if [ -f /etc/debian_version ]; then
    echo ">> Detected Debian/Ubuntu derivative."
    echo ">> Installing Clang, LLVM, LibBPF, and Kernel Headers..."
    sudo apt-get update -q
    sudo apt-get install -yq clang llvm libbpf-dev linux-headers-$(uname -r) build-essential libelf-dev python3-venv
elif [ -f /etc/arch-release ]; then
    echo ">> Detected Arch Linux."
    sudo pacman -Sy --noconfirm clang llvm libbpf linux-headers base-devel
elif [ -f /etc/fedora-release ]; then
    echo ">> Detected Fedora."
    sudo dnf install -y clang llvm libbpf-devel kernel-devel make
else
    echo -e "${RED}[!] WARNING: Unknown Distro. Assuming dependencies are manually installed.${NC}"
fi

# 2. COMPILING eBPF KERNEL MASK
echo -e "\n${GREEN}[2/4] COMPILING NETWORK MASK (eBPF)...${NC}"
XDP_SRC="network/xdp_outbound.c"
XDP_OBJ="network/xdp_outbound.o"

if [ -f "$XDP_SRC" ]; then
    echo ">> Compiling $XDP_SRC -> $XDP_OBJ"
    # The -target bpf is CRITICAL. Without it, it compiles as standard C and fails to load.
    clang -O2 -g -target bpf -c "$XDP_SRC" -o "$XDP_OBJ"
    
    if [ -f "$XDP_OBJ" ]; then
        echo -e ">> ${GREEN}SUCCESS: Kernel Object Compiled.${NC}"
    else
        echo -e ">> ${RED}FAILURE: Compilation command ran but output missing.${NC}"
        exit 1
    fi
else
    echo -e "${RED}[!] CRITICAL ERROR: $XDP_SRC not found.${NC}"
    echo "    Make sure you are in the root 'lucid-empire' directory."
    exit 1
fi

# 3. PYTHON ENVIRONMENT HARDENING
echo -e "\n${GREEN}[3/4] FINALIZING PYTHON ENVIRONMENT...${NC}"
if [ ! -d "venv" ]; then
    echo ">> Creating Virtual Environment..."
    python3 -m venv venv
fi

# Activate and install deps
source venv/bin/activate
if [ -f "gui_requirements.txt" ]; then
    echo ">> Installing GUI Dependencies..."
    pip install -r gui_requirements.txt
else
    echo ">> [INFO] gui_requirements.txt not found. Skipping pip install."
fi

# 4. PERMISSIONS & BINARY CHECK
echo -e "\n${GREEN}[4/4] PRE-FLIGHT CHECKS...${NC}"

# Check for Sovereign Binary
BIN_PATH="bin/firefox/firefox"
if [ -f "$BIN_PATH" ]; then
    echo -e ">> [OK] Sovereign Binary found at $BIN_PATH"
    chmod +x "$BIN_PATH"
else
    echo -e "${RED}[!] WARNING: Sovereign Browser Binary MISSING.${NC}"
    echo "    Expected at: ./$BIN_PATH  (or set LUCID_FIREFOX_BIN to an absolute path)"
    echo "    The system will build the Python Core, but launch will fail without the browser."
fi

# Fix executable permissions for scripts
chmod +x start_lucid.sh
chmod +x build_lucid_core.sh

echo -e "\n${CYAN}=================================================="
echo -e "   BUILD COMPLETE. SYSTEM READY."
echo -e "   TO LAUNCH: ./start_lucid.sh <PROFILE_UUID>"
echo -e "==================================================${NC}"
