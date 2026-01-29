import os
import sys
import subprocess
import argparse
import json
import logging
import platform
import time
from pathlib import Path
import glob
from core.profile_store import ProfileStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LUCID] - %(message)s')

IS_WINDOWS = platform.system().lower().startswith("win")
DEFAULT_FIREFOX_BIN = Path(os.environ.get("LUCID_FIREFOX_BIN", "./bin/firefox/firefox"))


def inject_proxy(profile_path, proxy_str):
    if not proxy_str:
        return
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


def load_profile(profile_id):
    store = ProfileStore()
    profile = store.get_profile(profile_id)
    if not profile:
        logging.error("Profile ID not found in database.")
        sys.exit(1)
    return normalize_profile(profile)


def normalize_profile(profile):
    """Ensure required keys exist for launcher consumption."""
    # Proxy
    profile.setdefault("proxy", profile.get("proxy_host"))
    # Template
    profile.setdefault("template", profile.get("template", "golden_template.json"))
    # Financial data
    if "financial" not in profile and "cc" in profile:
        profile["financial"] = profile["cc"]
    profile.setdefault("financial", {})
    # Mission block
    mission = profile.get("mission", {})
    if "target" in profile and "target_site" not in mission:
        mission["target_site"] = profile.get("target")
    if "aging" in profile and "aging_days" not in mission:
        try:
            mission["aging_days"] = int(profile.get("aging", 0))
        except Exception:
            mission["aging_days"] = 0
    mission.setdefault("target_site", mission.get("target_site", ""))
    mission.setdefault("aging_days", mission.get("aging_days", 0))
    profile["mission"] = mission
    return profile


def run_genesis(profile):
    temp_cfg = f"/tmp/{profile['id']}.json"
    with open(temp_cfg, 'w') as f:
        json.dump(profile, f)
    subprocess.run(["python3", "core/genesis_engine.py", "--profile_id", profile['id'], "--config", temp_cfg])
    if os.path.exists(temp_cfg):
        os.remove(temp_cfg)


def resolve_firefox_bin():
    env_path = os.environ.get("LUCID_FIREFOX_BIN")
    if env_path:
        p = Path(env_path)
        if p.exists():
            logging.info(f"Using LUCID_FIREFOX_BIN={p}")
            return p

    default_linux = Path("./bin/firefox/firefox")
    if default_linux.exists():
        return default_linux

    # Look for obj-*/dist/bin/firefox from local builds
    for candidate in glob.glob("obj-*/dist/bin/firefox"):
        p = Path(candidate)
        if p.exists():
            logging.info(f"Using discovered build artifact: {p}")
            return p

    if IS_WINDOWS:
        default_win = Path("./bin/firefox/firefox.exe")
        if default_win.exists():
            return default_win

    return None


def run_takeover(profile):
    logging.info("INITIATING TAKEOVER...")
    inject_proxy(profile['path'], profile.get('proxy'))

    env = os.environ.copy()
    env["FAKETIME"] = ""

    tmpl_path = f"lucid_profile_data/default/{profile['template']}"
    if not os.path.exists(tmpl_path):
        tmpl_path = "lucid_profile_data/default/golden_template.json"
        logging.warning(f"Using fallback golden template for profile {profile['id']}")

    with open(tmpl_path, 'r') as f:
        hw = json.load(f)

    env["LUCID_WEBGL_VENDOR"] = hw['webgl']['unmasked_vendor']
    env["LUCID_WEBGL_RENDERER"] = hw['webgl']['unmasked_renderer']
    env["LUCID_PLATFORM"] = hw['navigator']['platform']

    firefox_bin = resolve_firefox_bin()
    if not firefox_bin:
        logging.error("BINARY MISSING: Set LUCID_FIREFOX_BIN or place binary in ./bin/firefox/ (or obj-*/dist/bin/firefox)")
        sys.exit(127)

    cmd = [str(firefox_bin), "--profile", profile['path'], "--no-remote", "--new-instance"]
    # Skip Linux-only hooks (eBPF/Docker) on Windows; they are not invoked here by default
    subprocess.run(cmd, env=env)

    # Manual Takeover persistence loop: keep process alive while operator controls the browser
    logging.info(
        "BROWSER LAUNCHED. MANUAL TAKEOVER ACTIVE. Close terminal or Ctrl+C to terminate session."
    )
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("SHUTDOWN SEQUENCE INITIATED.")


def launch_sovereign_browser(profile):
    run_takeover(profile)


def main():
    parser = argparse.ArgumentParser(description="Lucid Empire Launcher")
    parser.add_argument("--mode", choices=["genesis", "takeover"], help="Legacy workflow mode")
    parser.add_argument("--profile_id", help="Profile UUID for legacy mode")
    parser.add_argument("--launch", help="Launch mode (triggered by start_lucid.sh)")
    args = parser.parse_args()

    if args.launch:
        profile = load_profile(args.launch)
        launch_sovereign_browser(profile)
        return

    if not args.mode or not args.profile_id:
        parser.print_help()
        return

    profile = load_profile(args.profile_id)
    if args.mode == "genesis":
        run_genesis(profile)
    elif args.mode == "takeover":
        run_takeover(profile)


if __name__ == "__main__":
    main()
