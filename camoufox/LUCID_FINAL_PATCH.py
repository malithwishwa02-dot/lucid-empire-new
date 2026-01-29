"""
LUCID EMPIRE :: MASTER INTEGRATION SUITE (v5.0 FINAL)
AUTHORITY: PROMETHEUS-CORE
OBJECTIVE: GAP CLOSURE & GUI DEPLOYMENT

ACTIONS:
1. Generates 'core/profile_store.py' (Identity Persistence).
2. Generates 'lucid_manager.py' (Commercial Dashboard).
3. Updates 'lucid_launcher.py' (Orchestration Link).
4. Generates 'start_lucid.sh' (One-Click Launch).
5. Verifies Biometric & Network modules.
"""

import os
import sys
import stat

# ==============================================================================
# 1. THE IDENTITY DATABASE (MISSING)
# ==============================================================================
PROFILE_STORE_CODE = """import json
import os
import uuid
import time

DB_FILE = "lucid_profiles.json"

class ProfileStore:
    def __init__(self):
        self._load_db()

    def _load_db(self):
        if not os.path.exists(DB_FILE):
            self.profiles = []
            self._save_db()
        else:
            with open(DB_FILE, 'r') as f:
                try:
                    self.profiles = json.load(f)
                except json.JSONDecodeError:
                    self.profiles = []

    def _save_db(self):
        with open(DB_FILE, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def create_profile(self, data):
        profile_id = str(uuid.uuid4())[:8]
        profile_path = os.path.join("lucid_profile_data", profile_id)
        os.makedirs(profile_path, exist_ok=True)

        new_profile = {
            "id": profile_id,
            "created_at": time.time(),
            "last_launched": None,
            "path": profile_path,
            "genesis_complete": False,
            **data 
        }
        
        self.profiles.append(new_profile)
        self._save_db()
        return new_profile

    def get_all(self):
        return self.profiles

    def get_profile(self, profile_id):
        return next((p for p in self.profiles if p['id'] == profile_id), None)

    def update_status(self, profile_id, key, value):
        for p in self.profiles:
            if p['id'] == profile_id:
                p[key] = value
        self._save_db()
        
    def delete_profile(self, profile_id):
        self.profiles = [p for p in self.profiles if p['id'] != profile_id]
        self._save_db()
"""

# ==============================================================================
# 2. THE COMMERCIAL GUI (MISSING)
# ==============================================================================
LUCID_MANAGER_CODE = """import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import json
import threading
from core.profile_store import ProfileStore

THEME = {"bg": "#121212", "fg": "#e0e0e0", "accent": "#00e676", "panel": "#1e1e1e"}

class LucidManager:
    def __init__(self, root):
        self.root = root
        self.root.title("LUCID EMPIRE :: OPS COMMANDER")
        self.root.geometry("1100x700")
        self.root.configure(bg=THEME["bg"])
        self.store = ProfileStore()
        self._setup_styles()
        self._layout_main()
        self.refresh_list()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=THEME["bg"])
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"], font=("Consolas", 10))
        style.configure("TButton", background="#333", foreground="white", borderwidth=1, font=("Consolas", 9, "bold"))
        style.map("TButton", background=[("active", "#444")])
        style.configure("Treeview", background=THEME["panel"], foreground="white", fieldbackground=THEME["panel"], rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#252526", foreground=THEME["accent"], font=("Consolas", 10, "bold"))

    def _layout_main(self):
        header = tk.Frame(self.root, bg="#000", height=60)
        header.pack(fill="x")
        tk.Label(header, text="PROMETHEUS-CORE | LINUX ENVIRONMENT", bg="#000", fg="#555").pack(side="top", anchor="e", padx=10)
        tk.Label(header, text="LUCID EMPIRE", bg="#000", fg="white", font=("Consolas", 18, "bold")).pack(side="left", padx=20, pady=10)
        tk.Button(header, text="[+] CREATE IDENTITY", bg=THEME["accent"], fg="#000", font=("Consolas", 10, "bold"), relief="flat", padx=15, command=self.open_create_dialog).pack(side="right", padx=20, pady=12)

        main_frame = tk.Frame(self.root, bg=THEME["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cols = ("name", "target", "aging", "status", "id")
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading("name", text="PERSONA (FULLZ)")
        self.tree.heading("target", text="TARGET SITE")
        self.tree.heading("aging", text="AGING DAYS")
        self.tree.heading("status", text="GENESIS STATE")
        self.tree.heading("id", text="UUID")
        self.tree.pack(fill="both", expand=True)

        controls = tk.Frame(self.root, bg="#222", height=80)
        controls.pack(fill="x")
        tk.Button(controls, text="⚛ INITIATE GENESIS", bg="#ff9800", fg="black", font=("Consolas", 11, "bold"), padx=20, pady=10, relief="flat", command=self.run_genesis).pack(side="left", padx=20, pady=15)
        tk.Button(controls, text="🚀 LAUNCH TAKEOVER", bg=THEME["accent"], fg="black", font=("Consolas", 11, "bold"), padx=20, pady=10, relief="flat", command=self.launch_browser).pack(side="right", padx=20, pady=15)

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.store.get_all():
            status = "Ready to Age" if not p['genesis_complete'] else "AGED (High Trust)"
            self.tree.insert("", "end", values=(p['name'], p['mission']['target_site'], f"{p['mission']['aging_days']} Days", status, p['id']))

    def open_create_dialog(self):
        top = tk.Toplevel(self.root)
        top.title("Generate High Trust Profile")
        top.geometry("600x700")
        top.configure(bg=THEME["bg"])
        nb = ttk.Notebook(top)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_id = tk.Frame(nb, bg=THEME["bg"])
        tab_net = tk.Frame(nb, bg=THEME["bg"])
        tab_fin = tk.Frame(nb, bg=THEME["bg"])
        tab_op = tk.Frame(nb, bg=THEME["bg"])
        nb.add(tab_id, text="1. IDENTITY"); nb.add(tab_net, text="2. NETWORK"); nb.add(tab_fin, text="3. FINANCIAL"); nb.add(tab_op, text="4. MISSION")

        def add_field(parent, label, r):
            tk.Label(parent, text=label, bg=THEME["bg"], fg="#888").grid(row=r, column=0, sticky="w", padx=20, pady=(15, 0))
            e = tk.Entry(parent, bg="#333", fg="white", relief="flat", insertbackground="white", width=40)
            e.grid(row=r+1, column=0, sticky="ew", padx=20, ipady=5)
            return e

        e_name = add_field(tab_id, "Full Name (Fullz)", 0)
        e_addr = add_field(tab_id, "Billing Address", 2)
        e_email = add_field(tab_id, "Email Address", 4)
        e_phone = add_field(tab_id, "Phone Number", 6)
        e_proxy = add_field(tab_net, "SOCKS5 Proxy (user:pass@ip:port)", 0)
        
        tk.Label(tab_net, text="Golden Template", bg=THEME["bg"], fg="#888").grid(row=2, column=0, sticky="w", padx=20, pady=(15,0))
        tmpl_combo = ttk.Combobox(tab_net, values=["golden_template.json"])
        if tmpl_combo['values']: tmpl_combo.set(tmpl_combo['values'][0])
        tmpl_combo.grid(row=3, column=0, sticky="ew", padx=20, ipady=5)

        e_cc_pan = add_field(tab_fin, "Card Number (PAN)", 1)
        e_cc_exp = add_field(tab_fin, "Expiry (MM/YY)", 3)
        e_cc_cvv = add_field(tab_fin, "CVV", 5)
        e_target = add_field(tab_op, "Target Website", 0)
        e_aging = add_field(tab_op, "Aging Period (Days)", 2); e_aging.insert(0, "66")

        def save():
            data = {
                "name": e_name.get(), "proxy": e_proxy.get(), "template": tmpl_combo.get(),
                "fullz": {"address": e_addr.get(), "email": e_email.get(), "phone": e_phone.get()},
                "financial": {"pan": e_cc_pan.get(), "exp": e_cc_exp.get(), "cvv": e_cc_cvv.get()},
                "mission": {"target_site": e_target.get(), "aging_days": int(e_aging.get() or 66)}
            }
            self.store.create_profile(data)
            self.refresh_list()
            top.destroy()
        tk.Button(tab_op, text="GENERATE PROFILE CONFIG", bg=THEME["accent"], fg="black", command=save).grid(row=5, column=0, pady=30)

    def run_genesis(self):
        sel = self.tree.selection()
        if not sel: return
        pid = self.tree.item(sel[0])['values'][4]
        # Using xterm to show the Genesis Engine output in a separate window
        cmd = f"xterm -e 'python3 lucid_launcher.py --mode genesis --profile_id {pid}; read -p \"Done\"'"
        subprocess.Popen(cmd, shell=True)
        self.store.update_status(pid, 'genesis_complete', True)
        self.root.after(2000, self.refresh_list)

    def launch_browser(self):
        sel = self.tree.selection()
        if not sel: return
        pid = self.tree.item(sel[0])['values'][4]
        # Launches the orchestrator in takeover mode
        subprocess.Popen(f"python3 lucid_launcher.py --mode takeover --profile_id {pid}", shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = LucidManager(root)
    root.mainloop()
"""

# ==============================================================================
# 3. THE UPDATED LAUNCHER (LINKING GUI -> ENGINE)
# ==============================================================================
LUCID_LAUNCHER_CODE = """import os
import sys
import subprocess
import argparse
import json
import logging
from core.profile_store import ProfileStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LUCID] - %(message)s')

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
            f.write("\\n".join(prefs))
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
        
        # Path to binary - Checks local bin first
        firefox_bin = "./bin/firefox/firefox" 
        if not os.path.exists(firefox_bin):
             logging.error("BINARY MISSING: Please place 'firefox' in ./bin/firefox/")
             sys.exit(1)

        cmd = [firefox_bin, "--profile", profile['path'], "--no-remote", "--new-instance"]
        subprocess.run(cmd, env=env)

if __name__ == "__main__":
    main()
"""

# ==============================================================================
# 4. THE ONE-CLICK START SCRIPT
# ==============================================================================
START_SCRIPT_CODE = """#!/bin/bash
echo "[*] LUCID EMPIRE INITIALIZATION..."
echo "[*] Installing GUI Dependencies..."
pip3 install tk --quiet
echo "[*] Launching Commander..."
python3 lucid_manager.py
"""

# ==============================================================================
# DEPLOYMENT LOGIC
# ==============================================================================
def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] GENERATED: {path}")

def main():
    print("LUCID EMPIRE :: PATCHING SYSTEM...")
    
    # 1. Deploy Database Module
    write_file("core/profile_store.py", PROFILE_STORE_CODE)
    
    # 2. Deploy GUI Manager
    write_file("lucid_manager.py", LUCID_MANAGER_CODE)
    
    # 3. Update Launcher
    write_file("lucid_launcher.py", LUCID_LAUNCHER_CODE)
    
    # 4. Deploy Start Script
    write_file("start_lucid.sh", START_SCRIPT_CODE)
    os.chmod("start_lucid.sh", stat.S_IRWXU)

    # 5. Verification
    print("\n[VERIFICATION]")
    if os.path.exists("modules/biometric_mimicry.py"):
        print("[+] Biometrics: DETECTED")
    else:
        print("[!] Biometrics: MISSING (Ensure modules/biometric_mimicry.py exists)")
        
    if os.path.exists("scripts/setup_fonts.sh"):
        print("[+] Font Script: DETECTED")
    else:
        print("[!] Font Script: MISSING (Ensure scripts/setup_fonts.sh exists)")

    print("\n[SUCCESS] SYSTEM PATCHED.")
    print("Usage: ./start_lucid.sh")

if __name__ == "__main__":
    main()
