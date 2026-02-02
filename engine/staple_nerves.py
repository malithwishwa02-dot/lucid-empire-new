"""
LUCID EMPIRE :: NERVE STAPLE v2.1
AUTHORITY: Dva.12
OBJECTIVE: Rewrite internal file references to match the Unified Architecture.
"""
import os
import sys


def patch_dashboard():
    target = "dashboard/main.py"
    if not os.path.exists(target):
        print(f"[!] MISSING: {target}")
        return

    print(f"[>] Patching {target}...")
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # FIX 1: Point subprocess calls to dashboard/main.py instead of lucid_launcher.py
    # We use relative path logic to ensure it runs from root
    new_content = content.replace("python3 lucid_launcher.py", "python3 dashboard/main.py")
    
    # FIX 2: Ensure correct imports if run directly
    if "sys.path.append" not in new_content:
        header = "import sys\nimport os\nsys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n"
        new_content = header + new_content

    if content != new_content:
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("    [+] Subprocess calls rerouted and sys.path updated.")
    else:
        print("    [=] Already patched.")


def patch_genesis():
    target = "core/genesis_engine.py"
    if not os.path.exists(target):
        print(f"[!] MISSING: {target}")
        return

    print(f"[>] Patching {target}...")
    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    # FIX 3: Allow Genesis Engine to see 'modules' folder when run as script
    if "sys.path.append" not in content:
        # Inject path fix before imports
        lines = content.split('\n')
        injection_point = 0
        for i, line in enumerate(lines):
            if line.startswith('import') or line.startswith('from'):
                injection_point = i
                break
        
        patch_code = [
            "import sys",
            "import os",
            "# Dva.12 Patch: Allow visibility of sibling modules",
            "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
            ""
        ]
        
        lines = lines[:injection_point] + patch_code + lines[injection_point:]
        new_content = "\n".join(lines)
        
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("    [+] Module visibility fixed.")
    else:
        print("    [=] Already patched.")


if __name__ == "__main__":
    print("[*] INITIATING NERVE STAPLE...")
    patch_dashboard()
    patch_genesis()
    print("[*] NERVOUS SYSTEM RE-CONNECTED.")