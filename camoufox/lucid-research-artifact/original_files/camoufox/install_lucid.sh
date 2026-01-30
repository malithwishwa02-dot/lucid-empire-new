#!/bin/bash
# LUCID EMPIRE :: AUTOMATED DEPLOYMENT PROTOCOL (HARDENED)
# PURPOSE: Platform-aware provisioning with venv, fonts, eBPF guardrails

set -euo pipefail

echo "=================================================="
echo "   LUCID EMPIRE :: INITIALIZING DEPLOYMENT"
echo "=================================================="

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

have_tty() { test -t 1; }
need_sudo() { command -v sudo >/dev/null 2>&1; }

ensure_root_or_sudo() {
  if [ "$EUID" -eq 0 ]; then return 0; fi
  if ! have_tty; then
    echo "[!] No TTY available for sudo prompt. Run from terminal or pre-authorize sudo." >&2
    exit 1;
  fi
  if need_sudo; then
    echo "[*] Elevating with sudo..."
    exec sudo "$0"
  else
    echo "[!] sudo not available. Please run as root." >&2
    exit 1
  fi
}

ensure_root_or_sudo

echo "[*] Installing system dependencies (Debian/Ubuntu expected)..."
apt-get update -qq
apt-get install -yq python3 python3-venv python3-pip python3-tk \
  clang llvm libelf-dev gcc-multilib docker.io docker-compose \
  linux-headers-$(uname -r) || apt-get install -yq linux-libc-dev

echo "[*] Pre-seeding Microsoft Core Fonts EULA..."
echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
apt-get install -yq ttf-mscorefonts-installer fonts-liberation2 || echo "[!] Font install skipped (non-Debian host)."
fc-cache -f -v || true

echo "[*] Preparing isolated Python environment (venv)..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f gui_requirements.txt ]; then pip install -r gui_requirements.txt; fi

echo "[*] Installing Playwright system dependencies (if available)..."
if command -v playwright >/dev/null 2>&1; then
  playwright install-deps || true
fi

echo "[*] Compiling network mask (XDP) with guardrails..."
XDP_SRC="network/xdp_outbound.c"
XDP_OBJ="network/xdp_outbound.o"
HEADER_PATH="/usr/src/linux-headers-$(uname -r)"
touch .no_ebpf || true
rm -f .no_ebpf
if [ -f "$XDP_SRC" ]; then
  if [ -d "$HEADER_PATH" ]; then
    clang -O2 -target bpf -I"$HEADER_PATH/include" -c "$XDP_SRC" -o "$XDP_OBJ" && echo "[*] eBPF compiled: $XDP_OBJ" || {
      echo "[!] eBPF compile failed; entering Lite Mode."; touch .no_ebpf; }
  else
    echo "[!] Kernel headers missing; skipping eBPF (Lite Mode)."; touch .no_ebpf
  fi
else
  echo "[!] $XDP_SRC not found; skipping eBPF."
  touch .no_ebpf
fi

echo "[*] Setting permissions..."
chmod +x start_lucid.sh lucid_launcher.py lucid_manager.py build_lucid_core.sh || true

if [ ! -f "bin/firefox/firefox" ]; then
    echo "[!] WARNING: Compiled Firefox binary missing in ./bin/firefox/"
    echo "    Run the GitHub workflow or place the binary manually."
fi

echo "=================================================="
echo "   DEPLOYMENT COMPLETE."
echo "   RUN: ./start_lucid.sh <PROFILE_UUID>"
echo "=================================================="