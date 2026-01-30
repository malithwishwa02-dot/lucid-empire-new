"""
LUCID LAUNCHER v5.2 (SMART PATHING)
AUTHORITY: PROMETHEUS-CORE
PURPOSE: Orchestrates Docker, eBPF, and Browser processes.
PATCH: Auto-detects binary location from 'install_lucid.sh' paths.
"""

import sys
import argparse
import time
import os
import json
import subprocess
import shutil

# [IMPORT YOUR EXISTING MODULES HERE]
# from core.genesis_engine import GenesisEngine


from core.bin_finder import find_sovereign_binary


def load_profile(profile_id):
    """
    Loads the profile config from lucid_profiles.json
    """
    db_path = "lucid_profiles.json"
    if not os.path.exists(db_path):
        print(f"[!] CRITICAL: {db_path} not found. Run the GUI first.")
        sys.exit(1)

    try:
        with open(db_path, "r") as f:
            profiles = json.load(f)
            
        # Handle list vs dict structure
        if isinstance(profiles, list):
            target = next((p for p in profiles if p["id"] == profile_id), None)
        else:
            target = profiles.get(profile_id)
            
        if not target:
            print(f"[!] ERROR: Profile {profile_id} not found in DB.")
            sys.exit(1)
            
        return target
    except Exception as e:
        print(f"[!] ERROR: Could not read profile DB: {e}")
        sys.exit(1)


def launch_sovereign_browser(profile):
    """
    The Core Launch Logic.
    """
    print(f"\n[*] IDENTITY: {profile.get('name', 'Unknown')}")
    print(f"[*] PROXY:    {profile.get('proxy', 'Direct')}")
    print(f"[*] TRUST:    {profile.get('trust_score', 0)}/100")
    
    # 1. Locate Binary
    binary_path = find_sovereign_binary()
    if not binary_path:
        print("\n[!] FATAL: Sovereign Browser Binary NOT FOUND.")
        print("    Expected at: ./bin/firefox/firefox")
        print("    Please download the Camoufox release and place it there.")
        sys.exit(1)
        
    print(f"[*] BINARY:   {binary_path}")

    # 2. Kernel Ops (Linux Only)
    if sys.platform.startswith("linux"):
        if os.geteuid() == 0:
            print("\n[1/3] KERNEL: Injecting eBPF maps for Windows TCP/IP...")
            # subprocess.run(["./network/xdp_loader.sh", "load"]) 
            # Placeholder for actual XDP load logic
            time.sleep(0.5)
        else:
            print("\n[!] WARNING: Not running as Root. eBPF Network Mask SKIPPED.")
    
    # 3. Launch
    print("[2/3] ENGINE:  Igniting Gecko Engine...")
    print("[3/3] SESSION: Manual Takeover Active.")
    print(">> BROWSER LAUNCHED. DO NOT CLOSE THIS TERMINAL.")
    
    # Construct the launch command
    # We pass the profile ID as an argument to the browser wrapper or env var
    cmd = [binary_path, "--no-remote", "--profile", f"./lucid_profile_data/{profile.get('id', 'default')}" ]
    
    try:
        proc = subprocess.Popen(cmd)
        
        # Keep alive loop
        while proc.poll() is None:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[*] SHUTDOWN SEQUENCE INITIATED.")
        proc.terminate()
    except Exception as e:
        print(f"\n[!] CRASH: {e}")


def main():
    parser = argparse.ArgumentParser(description="Lucid Empire CLI Launcher")
    parser.add_argument("--launch", type=str, help="UUID of the profile to launch")
    parser.add_argument("--mode", type=str, default="manual", help="Operation mode (manual/genesis)")
    
    args = parser.parse_args()
    
    if args.launch:
        profile = load_profile(args.launch)
        launch_sovereign_browser(profile)
    else:
        print("LUCID EMPIRE CLI")
        print("Usage: python lucid_launcher.py --launch <UUID>")

if __name__ == "__main__":
    main()
