"""
LUCID EMPIRE :: SYSTEM INTEGRITY DIAGNOSTIC
AUTHORITY: Dva.12
OBJECTIVE: Verify cross-module imports and structural coherence.
"""
import sys
import os
import importlib.util

# 1. Setup Environment
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

print(f"[*] ROOT DIRECTORY: {ROOT_DIR}")
print("[*] SCANNING VITAL ORGANS...\n")

modules_to_check = [
    ("core.genesis_engine", "Genesis Engine (Heart)"),
    ("modules.commerce_injector", "Commerce Module (Nerves)"),
    ("modules.biometric_mimicry", "Biometric Module (Motor Control)"),
    ("dashboard.main", "Dashboard (Brain)")
]

failures = 0

for module_path, description in modules_to_check:
    try:
        spec = importlib.util.find_spec(module_path)
        if spec is None:
            raise ImportError
        print(f"  [PASS] {description:30} ... DETECTED")
    except ImportError:
        print(f"  [FAIL] {description:30} ... NOT FOUND")
        failures += 1
    except Exception as e:
        print(f"  [FAIL] {description:30} ... ERROR: {e}")
        failures += 1

print("\n---------------------------------------------------")
if failures == 0:
    print("[*] SYSTEM STATUS: INTEGRAL. READY FOR IGNITION.")
    sys.exit(0)
else:
    print(f"[!] SYSTEM STATUS: CRITICAL FAILURE ({failures} errors).")
    print("    Did you run 'unify_empire.sh' and 'staple_nerves.py'?")
    sys.exit(2)
