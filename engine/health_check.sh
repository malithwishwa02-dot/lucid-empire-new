#!/bin/bash
# LUCID EMPIRE :: HEALTH CHECK
# Verifies venv, kernel headers, fonts, binary, and eBPF status.

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

# 1) Venv
if [ -f "venv/bin/activate" ]; then
  pass "Virtualenv present."
else
  warn "venv missing. Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install -r gui_requirements.txt"
fi

# 2) Kernel headers
KREL="$(uname -r)"
HEADER_PATH="/usr/src/linux-headers-$KREL"
if [ -d "$HEADER_PATH" ]; then
  pass "Kernel headers found: $HEADER_PATH"
else
  warn "Kernel headers missing for $KREL. Install linux-headers-$KREL or linux-libc-dev."
fi

# 3) Fonts (basic check: presence of Microsoft core cache)
if fc-list | grep -qi "segoe\|calibri"; then
  pass "Microsoft core fonts detected."
else
  warn "Fonts not detected. Install ttf-mscorefonts-installer (EULA preseed) or run install_lucid.sh."
fi

# 4) Firefox binary
if [ -f "bin/firefox/firefox" ] || [ -f "bin/firefox/firefox.exe" ]; then
  pass "Firefox binary present in ./bin/firefox/"
else
  # try build outputs
  found_build="$(find . -path "./obj-*/dist/bin/firefox" -o -path "./obj-*/dist/bin/firefox.exe" | head -n1 || true)"
  if [ -n "$found_build" ]; then
    warn "Binary not in ./bin/firefox, but found build artifact: $found_build"
  else
    fail "Firefox binary missing. Set LUCID_FIREFOX_BIN or place binary in ./bin/firefox/."
  fi
fi

# 5) eBPF status / WSL detection
is_wsl=0
if grep -qi "microsoft" /proc/version 2>/dev/null; then is_wsl=1; fi
if [ -f ".no_ebpf" ]; then
  warn "Lite Mode: .no_ebpf present (eBPF disabled)."
elif [ $is_wsl -eq 1 ]; then
  warn "WSL detected; eBPF/XDP typically unavailable. Consider touching .no_ebpf to skip."
else
  pass "eBPF not disabled. Ensure headers/capabilities allow XDP."
fi

echo "-- Health check complete --"
