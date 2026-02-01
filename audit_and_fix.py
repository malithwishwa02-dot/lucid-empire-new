import os
import sys
import subprocess
import shutil
from pathlib import Path

# --- CONFIGURATION ---
REQUIRED_DIRS = [
    "lucid_profile_data",
    "network",
    "core",
    "modules",
    "patches"
]

REQUIRED_FILES = {
    "network/xdp_outbound.c": "CRITICAL: Kernel masking source code missing.",
    "lucid_profile_data/default/golden_template.json": "CRITICAL: Golden Identity Template missing.",
    "core/genesis_engine.py": "CRITICAL: Genesis logic missing."
}

def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "WARN": "\033[93m", "CRIT": "\033[91m", "OK": "\033[92m", "RESET": "\033[0m"}
    print(f"{colors.get(level, '')}[{level}] {msg}{colors['RESET']}")

def check_environment():
    """Phase 1: Environment Integrity Check"""
    log("Scanning directory structure...", "INFO")
    
    missing_items = []
    for d in REQUIRED_DIRS:
        if not os.path.exists(d):
            log(f"Missing Directory: {d}", "WARN")
            os.makedirs(d, exist_ok=True)
            log(f"Created: {d}", "OK")

    for f_path, error_msg in REQUIRED_FILES.items():
        if not os.path.exists(f_path):
            log(f"{error_msg} ({f_path})", "CRIT")
            missing_items.append(f_path)
    
    if missing_items:
        log("Environment corrupted. Restore missing assets.", "CRIT")
        return False
    return True

def compile_xdp_module():
    """Phase 2: Compiling the Fail-Closed Network Shield"""
    log("Compiling XDP Kernel Module...", "INFO")
    
    c_source = "network/xdp_outbound.c"
    o_output = "network/xdp_outbound.o"
    
    # Check for clang/llvm
    if shutil.which("clang") is None:
        log("CLANG not found. Cannot compile eBPF filters.", "CRIT")
        log("Install: sudo apt install clang llvm libelf-dev gcc-multilib", "INFO")
        return

    cmd = [
        "clang", "-O2", "-target", "bpf", "-c", c_source, "-o", o_output
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(o_output):
            log("XDP Module Compiled Successfully.", "OK")
        else:
            log("Compilation failed silently.", "CRIT")
    except subprocess.CalledProcessError as e:
        log(f"Compilation Error: {e}", "CRIT")

def scan_for_placeholders():
    """Phase 3: Codebase Hygiene"""
    log("Scanning for TODOs and Placeholders...", "INFO")
    
    scan_ext = [".py", ".js", ".c", ".md"]
    keywords = ["TODO", "PASTE_HERE", "MOCK", "FIXME", "pass  #"]
    
    for root, _, files in os.walk("."):
        if "node_modules" in root or "venv" in root or ".git" in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in scan_ext):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            for kw in keywords:
                                if kw in line:
                                    log(f"Found {kw} in {path}:{i}", "WARN")
                                    log(f"  -> {line.strip()}", "INFO")
                except Exception as e:
                    pass

def finalize_setup():
    """Phase 4: Permission Fixes"""
    log("Setting execution permissions...", "INFO")
    scripts = ["network/xdp_loader.sh", "install_lucid.sh", "start_lucid.sh"]
    for s in scripts:
        if os.path.exists(s):
            try:
                os.chmod(s, 0o755)
                log(f"Executable: {s}", "OK")
            except:
                log(f"Failed to set permissions for: {s}", "WARN")

if __name__ == "__main__":
    print("""
    ░░      ░░  ░░  ░░░░░░  ░░  ░░░░░░  
    ▒▒      ▒▒  ▒▒  ▒▒      ▒▒  ▒▒   ▒▒ 
    ▓▓      ▓▓  ▓▓  ▓▓      ▓▓  ▓▓   ▓▓ 
    ██      ██  ██  ██      ██  ██   ██ 
    ██████   ████   ██████  ██  ██████  
       [ AUDIT & REMEDIATION v1.0 ]
    """)
    
    if check_environment():
        compile_xdp_module()
        scan_for_placeholders()
        finalize_setup()
        log("System is OP-READY. Execute 'python lucid_api.py' to start the backend.", "OK")
    else:
        log("Critical assets missing. Aborting.", "CRIT")
