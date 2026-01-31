"""
LUCID EMPIRE :: MASTER IGNITION SEQUENCE
AUTHORITY: Dva.12
USAGE: python3 start_empire.py
"""
import os
import sys
import subprocess
import time


def banner():
    print(r"""
    ██╗     ██╗   ██╗ ██████╗██╗██████╗ 
    ██║     ██║   ██║██╔════╝██║██╔══██╗
    ██║     ██║   ██║██║     ██║██║  ██║
    ██║     ██║   ██║██║     ██║██║  ██║
    ███████╗╚██████╔╝╚██████╗██║██████╔╝
    ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═════╝ 
        SOVEREIGN ANTI-DETECT SUITE
           AUTHORITY: Dva.12
    """)


def check_requirements():
    print("[*] Checking environment...")
    required = ["playwright", "customtkinter", "fake_useragent"]
    missing = []
    import importlib.util
    for package in required:
        if importlib.util.find_spec(package) is None:
            missing.append(package)
    
    if missing:
        print(f"[!] MISSING DEPENDENCIES: {', '.join(missing)}")
        print("    Auto-installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("[+] Dependencies installed.")
    else:
        print("[+] Environment verified.")


def ignite():
    banner()
    check_requirements()
    
    # Ensure root is in path
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(root_dir)
    
    dashboard_path = os.path.join(root_dir, "dashboard", "main.py")
    
    if not os.path.exists(dashboard_path):
        print("[!] CRITICAL: Dashboard not found at dashboard/main.py")
        print("    Falling back to root search...")
        if os.path.exists("lucid_launcher.py"):
            dashboard_path = "lucid_launcher.py"
        else:
            print("[!] FATAL: No launcher found.")
            sys.exit(1)

    print(f"[*] LAUNCHING TARGET: {dashboard_path}")
    print("[*] OBLIVION GATES OPENING...")
    time.sleep(1)
    
    # Execute the dashboard
    try:
        # Use current Python interpreter to run the dashboard script
        subprocess.run([sys.executable, dashboard_path])
    except KeyboardInterrupt:
        print("\n[*] SHUTDOWN SEQUENCE INITIATED.")


if __name__ == "__main__":
    ignite()
