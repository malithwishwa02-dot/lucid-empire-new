import tkinter as tk
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
