#!/bin/bash
# LUCID EMPIRE :: LAUNCH PROTOCOL v5.0 (HARDENED)
# FUNCTION: Platform-aware handoff with eBPF Lite Mode guard

set -euo pipefail

PROFILE_ID=${1:-}
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "=================================================="
echo "   LUCID EMPIRE :: LAUNCH SEQUENCE INITIATED"
echo "   TARGET PROFILE: ${PROFILE_ID:-<none>}"
echo "=================================================="

if [ -z "$PROFILE_ID" ]; then
    echo "[!] ERROR: No Profile ID received from Commander."
    echo "    USAGE: ./start_lucid.sh <UUID>"
    exit 1
fi

NO_EBPF_MARKER=".no_ebpf"
IS_WSL=0
if grep -qi "microsoft" /proc/version 2>/dev/null; then IS_WSL=1; fi

have_tty() { test -t 1; }

maybe_escalate() {
  if [ -f "$NO_EBPF_MARKER" ]; then
    echo "[*] Lite Mode active (.no_ebpf present). Skipping sudo/eBPF."
    return 0
  fi
  if [ "$IS_WSL" -eq 1 ]; then
    echo "[*] WSL detected; eBPF unsupported. Touching .no_ebpf and continuing in Lite Mode."
    touch "$NO_EBPF_MARKER"
    return 0
  fi
  if [ "$EUID" -eq 0 ]; then
    echo "[*] STATUS: ROOT ACCESS GRANTED."
    return 0
  fi
  if ! have_tty; then
    echo "[!] No TTY for sudo prompt. Either run from terminal or touch .no_ebpf to skip escalation." >&2
    exit 1
  fi
  echo "[*] ESCALATION: Requesting sudo for eBPF load..."
  exec sudo "$0" "$PROFILE_ID"
}

maybe_escalate

if [ ! -f "$NO_EBPF_MARKER" ]; then
  echo "[*] NET: Loading XDP Packet Mask (Windows 10 Signature) ..."
  # Loader is expected inside Python; sudo context ensures capability
else
  echo "[*] NET: Lite Mode (no eBPF). Proceeding without kernel hooks."
fi

if [ -f "venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

if [ -f "lucid_launcher.py" ]; then
    python3 lucid_launcher.py --launch "$PROFILE_ID" --mode manual
else
    echo "[!] CRITICAL: lucid_launcher.py not found in current directory."
    echo "    PATH: $(pwd)"
    exit 1
fi

echo "[*] SESSION TERMINATED."
