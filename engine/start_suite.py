import os
import sys

# Add subdirectories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'dashboard'))

try:
    import main as dashboard
    print("[*] Launching Lucid Empire Dashboard...")
    dashboard.main()
except ImportError as e:
    print(f"[!] Critical Error: {e}")
    print("[*] Attempting fallback to legacy launcher...")
    os.system("python3 dashboard/main.py")
