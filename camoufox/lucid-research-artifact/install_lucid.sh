#!/bin/bash
# ==============================================================================
# LUCID EMPIRE :: ONE-CLICK DEPLOYMENT VECTOR
# AUTHORITY: Dva.12 | STATUS: CLASSIFIED
# TARGET: Linux (Debian/Ubuntu 22.04/24.04)
# ==============================================================================

# 1. PRIVILEGE & OS CHECK
if [ "$EUID" -ne 0 ]; then
  echo "[!] CRITICAL: Run as root (sudo ./install_lucid.sh)"
  exit 1
fi

echo "[*] INITIATING OBLIVION PROTOCOL..."
echo "[*] TARGET: HOST SYSTEM PREP & FINGERPRINT HYGIENE"

# 2. SYSTEM DEPENDENCY INJECTION
# Automating the EULA acceptance for Microsoft Fonts to prevent script hanging.
echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections

echo "[*] INSTALLING CRITICAL LIBRARIES (GTK, X11, ALSA)..."
apt-get update && apt-get install -y \
    python3 python3-venv python3-pip \
    xvfb libgtk-3-0 libasound2 libdbus-glib-1-2 \
    libx11-xcb1 libxt6 libgbm1 libdrm2 \
    libfreetype6 fontconfig \
    ttf-mscorefonts-installer \
    curl unzip

# 3. FONT HYGIENE (Anti-Enumeration)
# Rebuilding font cache to ensure the new MS fonts are visible to the browser engine.
echo "[*] REBUILDING FONT CACHE..."
fc-cache -f -v > /dev/null

# 4. ENVIRONMENT ISOLATION
if [ ! -d "lucid_env" ]; then
    echo "[*] CREATING PYTHON VIRTUAL ENVIRONMENT..."
    python3 -m venv lucid_env
fi

# Activate Environment for subsequent commands
source lucid_env/bin/activate

# 5. CORE ARSENAL INSTALLATION
echo "[*] INSTALLING LUCID ENGINE (Camoufox + Browserforge)..."
pip install --upgrade pip
# [geoip] is mandatory for Timezone/Locale spoofing
pip install "camoufox[geoip]" browserforge playwright

# 6. BINARY BRIDGE (The Fetch)
echo "[*] FETCHING MODIFIED BROWSER BINARY..."
python3 -m camoufox fetch

# 7. CONFIGURATION INJECTION (The Malithwishwa Patch)
# Generates a production-ready entry point with memory leaks & CPU bugs patched.
echo "[*] GENERATING LAUNCH KERNEL (main.py)..."

cat << 'EOF' > main.py
import asyncio
import random
from camoufox import AsyncNewContext

# LUCID EMPIRE CONFIGURATION
# Based on 'malithwishwa02-dot' patches for stability and evasion.
LUCID_CONFIG = {
    # CRITICAL: "virtual" spawns Xvfb. Standard "headless" = Instant Detection.
    "headless": "virtual",  
    
    # OS Spoofing: Matches the injected fonts (Arial/Times New Roman)
    "os": ["windows", "macos"],
    
    # Internal Preferences
    "config": {
        # FIX: Issue #123 (Night Sky High CPU Usage)
        "browser.theme.content-theme": 0,
        
        # FIX: Issue #87 (Memory Leak Mitigation)
        "browser.cache.memory.enable": False,
        "javascript.options.mem.gc_frequency": 10,
        "image.mem.decode_bytes_at_a_time": 4096,
        
        # EVASION: Disable WebRTC Leaks
        "media.peerconnection.enabled": False,
    },
    
    # Behavior & Networking
    "humanize": True,  # Smooth mouse movements
    "geoip": True      # Sync Timezone/Locale to IP
}

async def ignite():
    print(f"[*] LUCID ENGINE STARTING...")
    print(f"[*] MODE: VIRTUAL DISPLAY (XVFB)")
    
    try:
        async with AsyncNewContext(**LUCID_CONFIG) as context:
            page = await context.new_page()
            
            print("[*] TARGET: CREEPJS FINGERPRINT ANALYSIS")
            await page.goto("https://abrahamjuliot.github.io/creepjs/", timeout=60000)
            
            # Simulate basic entropy
            await page.mouse.wheel(0, 500)
            await asyncio.sleep(5)
            
            # Extract Trust Score (Simple validation)
            score = await page.evaluate("() => document.querySelector('.grade-A, .grade-B, .grade-C')?.innerText || 'Unknown'")
            print(f"[+] SELF-TEST COMPLETE. TRUST GRADE: {score}")
            
            await page.screenshot(path="lucid_verification.png")
            print("[+] SCREENSHOT SAVED: lucid_verification.png")
            
    except Exception as e:
        print(f"[!] CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(ignite())
EOF

# 8. PERMISSIONS & FINALIZATION
chmod +x main.py
# Fix ownership if sudo created files owned by root
if [ -n "$SUDO_USER" ]; then
    chown -R $SUDO_USER:$SUDO_USER lucid_env main.py
fi

echo "[*] DEPLOYMENT COMPLETE."
echo "[*] COMMAND TO ENGAGE:"
echo "    source lucid_env/bin/activate"
echo "    python3 main.py"
echo "======================================================"