import os
import re
from pathlib import Path

# --- TARGET CONFIGURATION ---
EXPECTATIONS = {
    "GUI_BRIDGE": ["lucid_api.py", "FastAPI backend to link Python core to React"],
    "GUI_FRONTEND": ["src-tauri/tauri.conf.json", "Tauri/React Commercial UI"],
    "KERNEL_SHIELD": ["network/xdp_loader.sh", "Script to load eBPF hooks"],
    "TIME_MACHINE": ["core/time_displacement.py", "Logic to backdate filesystem mtime"],
    "IDENTITY_LOBOTOMY": ["lucid_profile_data/default/golden_template.json", "Real-world fingerprint source"]
}

FORBIDDEN_PATTERNS = [
    r"TODO", 
    r"FIXME", 
    r"pass\s*#", 
    r"mock_", 
    r"print\(\"test\"\)"
]

def scan_gaps():
    print(f"[*] SCANNING FOR ARCHITECTURAL GAPS...")
    missing_critical = []
    
    for key, (path, desc) in EXPECTATIONS.items():
        if not os.path.exists(path):
            print(f"  [MISSING] {key}: {path}")
            print(f"     -> Impact: {desc}")
            missing_critical.append(key)
        else:
            print(f"  [OK]      {key}")

    return missing_critical

def scan_code_issues():
    print(f"\n[*] SCANNING FOR CODE SMELLS & PLACEHOLDERS...")
    
    for root, _, files in os.walk("."):
        if "node_modules" in root or ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if not file.endswith((".py", ".js", ".c", ".sh", ".rs")): 
                continue
                
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        for pattern in FORBIDDEN_PATTERNS:
                            if re.search(pattern, line):
                                print(f"  [ISSUE] {file}:{i+1} -> {line.strip()}")
            except: pass

def check_structure():
    print(f"\n[*] ANALYZING REPOSITORY FRAGMENTATION...")
    archives = [f for f in os.listdir('.') if f.endswith('.zip')]
    if len(archives) > 0:
        print(f"  [WARN] Found {len(archives)} ZIP archives in root. Project is fragmented.")
        print(f"     -> Recommended: Extract 'lucid-empire-research-v2' and promote to root.")
    else:
        print("  [OK] No ZIP archives found in root.")

if __name__ == "__main__":
    print("=== LUCID EMPIRE: ZERO-DETECT AUDIT ===")
    missing = scan_gaps()
    scan_code_issues()
    check_structure()
    
    print("\n=== SUMMARY ===")
    if missing:
        print(f"SYSTEM NOT OPS-READY. Missing components: {', '.join(missing)}")
    else:
        print("SYSTEM ARCHITECTURE VALID. Proceed to compilation.")
