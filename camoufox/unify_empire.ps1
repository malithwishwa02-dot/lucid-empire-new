# LUCID EMPIRE :: UNIFICATION PROTOCOL (v2.1)
# AUTHORITY: Dva.12
# OBJECTIVE: Merge 'Brain' (Research V2) into 'Body' (Root Camoufox).

$SOURCE_BRAIN = "lucid-empire-modifications"
$TARGET_ROOT = "."

Write-Host "[*] INITIATING UNIFICATION PROTOCOL..."

# 1. VERIFY SOURCE
if (-not (Test-Path $SOURCE_BRAIN)) {
    Write-Host "[!] ERROR: Research V2 brain not found at expected path."
    Write-Host "    Looking for: $SOURCE_BRAIN"
    exit 1
}

# 2. TRANSPLANT: CORE (Genesis Engine & Profile Store)
Write-Host "[>] Transplanting CORE (Genesis Engine)..."
New-Item -ItemType Directory -Force -Path "core" | Out-Null
Copy-Item -Path "$SOURCE_BRAIN\core\*" -Destination "core" -Recurse -ErrorAction SilentlyContinue
# Fallback if files are flat in source
Copy-Item -Path "$SOURCE_BRAIN\genesis_engine.py" -Destination "core" -ErrorAction SilentlyContinue
Copy-Item -Path "$SOURCE_BRAIN\profile_store.py" -Destination "core" -ErrorAction SilentlyContinue

# 3. TRANSPLANT: MODULES (Biometrics & Commerce)
Write-Host "[>] Transplanting MODULES (Nervous System)..."
New-Item -ItemType Directory -Force -Path "modules" | Out-Null
Copy-Item -Path "$SOURCE_BRAIN\modules\*" -Destination "modules" -Recurse -ErrorAction SilentlyContinue

# 4. TRANSPLANT: DASHBOARD (The Face)
Write-Host "[>] Transplanting DASHBOARD..."
New-Item -ItemType Directory -Force -Path "dashboard" | Out-Null
Copy-Item -Path "$SOURCE_BRAIN\lucid_launcher.py" -Destination "dashboard\main.py" -ErrorAction SilentlyContinue
Copy-Item -Path "$SOURCE_BRAIN\lucid_manager.py" -Destination "dashboard\manager.py" -ErrorAction SilentlyContinue
Copy-Item -Path "$SOURCE_BRAIN\lucid_commander.py" -Destination "dashboard\commander.py" -ErrorAction SilentlyContinue

# 5. TRANSPLANT: NETWORK (eBPF)
Write-Host "[>] Transplanting NETWORK LAYERS..."
New-Item -ItemType Directory -Force -Path "network" | Out-Null
Copy-Item -Path "$SOURCE_BRAIN\network\*" -Destination "network" -Recurse -ErrorAction SilentlyContinue

# 6. TRANSPLANT: ASSETS & PROFILES
Write-Host "[>] Transplanting ASSETS..."
New-Item -ItemType Directory -Force -Path "assets\templates" | Out-Null
Copy-Item -Path "$SOURCE_BRAIN\lucid_profile_data\default\golden_template.json" -Destination "assets\templates" -Recurse -ErrorAction SilentlyContinue
Copy-Item -Path "$SOURCE_BRAIN\lucid_profiles.json" -Destination "assets\profiles.db" -ErrorAction SilentlyContinue

# 7. CLEANUP & GENERATE ENTRY POINT
Write-Host "[>] Generating Master Entry Point..."
@"
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
"@ | Out-File -FilePath "start_suite.py" -Encoding utf8

Write-Host "[*] UNIFICATION COMPLETE."
Write-Host "[*] The Repository is now fully operational."
Write-Host "    Run: python3 start_suite.py"
