import os
import sys
import subprocess
import argparse
import json
import logging
from core.profile_store import ProfileStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LUCID] - %(message)s')

# Detect if running as an installed Debian package and adjust paths/env accordingly
# - Add bundled Python libs to `sys.path` so the packaged dependencies are used
# - Set `LUCID_FIREFOX_BIN` for the packaged firefox binary
if os.path.exists("/opt/lucid-empire/browser/firefox"):
    pylibs_path = "/opt/lucid-empire/pylibs"
    if pylibs_path not in sys.path:
        sys.path.insert(0, pylibs_path)
    os.environ.setdefault("LUCID_FIREFOX_BIN", "/opt/lucid-empire/browser/firefox")


def inject_proxy(profile_path, proxy_str):
    if not proxy_str: return
    try:
        if "@" in proxy_str:
            auth, endpoint = proxy_str.split("@")
            ip, port = endpoint.split(":")
        else:
            ip, port = proxy_str.split(":")
            
        prefs = [
            'user_pref("network.proxy.type", 1);',
            f'user_pref("network.proxy.socks", "{ip}");',
            f'user_pref("network.proxy.socks_port", {port});',
            'user_pref("network.proxy.socks_remote_dns", true);'
        ]
        user_js = os.path.join(profile_path, "user.js")
        with open(user_js, "a") as f:
            f.write("\n".join(prefs))
        logging.info(f"PROXY INJECTED: {ip}")
    except Exception as e:
        logging.error(f"Proxy Error: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["genesis", "takeover"])
    parser.add_argument("--profile_id", required=True)
    args = parser.parse_args()

    store = ProfileStore()
    profile = store.get_profile(args.profile_id)
    if not profile:
        logging.error("Profile ID not found in database.")
        sys.exit(1)

    if args.mode == "genesis":
        # Create temp config for Genesis Engine
        temp_cfg = f"/tmp/{args.profile_id}.json"
        with open(temp_cfg, 'w') as f:
            json.dump(profile, f)
        # Execute Genesis Engine
        subprocess.run(["python3", "core/genesis_engine.py", "--profile_id", args.profile_id, "--config", temp_cfg])
        if os.path.exists(temp_cfg): os.remove(temp_cfg)

    elif args.mode == "takeover":
        logging.info("INITIATING TAKEOVER...")
        inject_proxy(profile['path'], profile.get('proxy'))
        
        # Load Hardware Mask
        tmpl_path = f"lucid_profile_data/default/{profile['template']}"
        if not os.path.exists(tmpl_path):
             # Fallback if template path logic differs
             tmpl_path = "lucid_profile_data/default/golden_template.json"

        with open(tmpl_path, 'r') as f:
            hw = json.load(f)
            
        env = os.environ.copy()
        env["FAKETIME"] = "" # Disable Time Warp for Live Op
        env["LUCID_WEBGL_VENDOR"] = hw['webgl']['unmasked_vendor']
        env["LUCID_WEBGL_RENDERER"] = hw['webgl']['unmasked_renderer']
        env["LUCID_PLATFORM"] = hw['navigator']['platform']
        
        # Path to binary - Prefer packaged binary via LUCID_FIREFOX_BIN, fallback to local ./bin
        firefox_bin = os.environ.get("LUCID_FIREFOX_BIN", "./bin/firefox/firefox")
        if not os.path.exists(firefox_bin):
            logging.error(f"BINARY MISSING: {firefox_bin} not found. Please place 'firefox' in ./bin/firefox/ or install the package.")
            sys.exit(1)

        cmd = [firefox_bin, "--profile", profile['path'], "--no-remote", "--new-instance"]
        subprocess.run(cmd, env=env)

if __name__ == "__main__":
    main()
