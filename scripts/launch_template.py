#!/usr/bin/env python3
"""
launch_template.py - minimal launch/self-test helper for Lucid Empire
Usage: python launch_template.py --config /path/to/camoufox_config.json [--selftest]
"""
import argparse
import json
import os
import sys
from pathlib import Path

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def launch_with_camoufox(config):
    try:
        import camoufox
    except Exception as e:
        print(f"camoufox package not available: {e}")
        return False
    # Best-effort: use camoufox API if available
    try:
        cam = camoufox.Launcher(config)
        browser = cam.launch()
        p = browser.new_page()
        p.goto('https://abrahamjuliot.github.io/creepjs/')
        p.screenshot(path='creepjs_camoufox.png', full_page=True)
        print('SCREENSHOT_SAVED: creepjs_camoufox.png')
        browser.close()
        return True
    except Exception as e:
        print(f"Error launching camoufox: {e}")
        return False


def launch_with_playwright(config):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        print(f"playwright not available: {e}")
        return False
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, args=['--no-sandbox'])
        page = browser.new_page()
        page.goto('https://abrahamjuliot.github.io/creepjs/')
        page.screenshot(path='creepjs_playwright.png', full_page=True)
        print('SCREENSHOT_SAVED: creepjs_playwright.png')
        browser.close()
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Config not found: {cfg_path}")
        sys.exit(2)

    cfg = load_config(cfg_path)
    ok = launch_with_camoufox(cfg)
    if not ok and args.selftest:
        ok = launch_with_playwright(cfg)

    if not ok:
        print('Launch failed')
        sys.exit(1)
    print('Launch succeeded')

if __name__ == '__main__':
    main()
