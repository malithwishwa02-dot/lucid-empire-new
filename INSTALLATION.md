# Lucid Empire - Installation Guide

Complete step-by-step installation instructions for all platforms.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Install (All Platforms)](#quick-install)
3. [Detailed Setup Instructions](#detailed-setup-instructions)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor (Intel/AMD/Apple Silicon)
- **RAM**: 4GB (8GB+ recommended)
- **Storage**: 5GB free space (for cloned repo + engine)
- **OS**: Windows 10+, Linux (Ubuntu 20.04+, Fedora 33+), macOS 10.15+
- **Python**: 3.10+ (3.11+ recommended)
- **Git**: 2.30+
- **Browser**: Firefox 147+ (included)

### Internet Connection
- **Bandwidth**: 500MB+ for initial clone + engine download
- **Network**: Stable connection (resumable downloads supported)

### Optional Dependencies
- **PowerShell 7+** (Windows, for better compatibility)
- **curl** or **wget** (for post-clone binary restoration)
- **tar** (for archive extraction; built into macOS/Linux, available via WSL on Windows)

---

## Quick Install

### Option A: Fastest (Recommended)

**All Platforms:**
```bash
# Clone the repository
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new

# Enable auto-setup hook (future clones will auto-restore)
git config core.hooksPath .githooks

# Run setup to download externals
./setup_externals.sh           # Linux/macOS
# OR
.\setup_externals.ps1          # Windows PowerShell

# Install Python dependencies
pip install -r requirements.txt

# Launch
python main.py
```

### Option B: Automated Setup (Windows)

```powershell
# Clone
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new

# Run setup PowerShell script
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup_externals.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Launch
python main.py
```

### Option C: Automated Setup (Linux/macOS)

```bash
# Clone
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new

# Run setup shell script
chmod +x setup_externals.sh
./setup_externals.sh

# Install dependencies
pip install -r requirements.txt

# Launch
python main.py
```

---

## Detailed Setup Instructions

### 1. Clone Repository

**SSH (if configured):**
```bash
git clone git@github.com:malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new
```

**HTTPS (no keys required):**
```bash
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new
```

**Shallow Clone (faster for first-time):**
```bash
git clone --depth=1 https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new
git fetch --unshallow  # Later, when you want full history
```

### 2. Setup External Dependencies

The repository uses lazy-loaded external dependencies (engine/, bin/) to keep initial clone size small (~100MB instead of ~2.6GB).

#### Windows PowerShell

```powershell
cd lucid-empire-new

# Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Run setup script
.\setup_externals.ps1

# Optional flags:
# .\setup_externals.ps1 -Force              # Re-download even if exists
# .\setup_externals.ps1 -ReleaseVersion v1.0  # Use specific version
```

**Expected Output:**
```
╔════════════════════════════════════════════════════════════════════╗
║  Lucid Empire - External Dependencies Setup                        ║
║  Downloading: engine/ and bin/ folders                             ║
╚════════════════════════════════════════════════════════════════════╝

✓ Prerequisites verified
✓ Found release: v1.0.0
✓ Downloaded: engine.tar.gz
✓ Extracted: engine.tar.gz
✓ Downloaded: bin.tar.gz
✓ Extracted: bin.tar.gz

✓ Setup complete!
Ready to run: python main.py
```

#### Linux/macOS Shell

```bash
cd lucid-empire-new
chmod +x setup_externals.sh
./setup_externals.sh

# Optional flags:
# ./setup_externals.sh --force              # Re-download even if exists
# ./setup_externals.sh --version v1.0.0     # Use specific version
```

#### Manual Download (if scripts fail)

1. Visit GitHub Releases: https://github.com/malithwishwa02-dot/lucid-empire-new/releases
2. Download `engine.tar.gz` and `bin.tar.gz`
3. Extract to repository root:
   ```bash
   tar -xzf engine.tar.gz
   tar -xzf bin.tar.gz
   ```

### 3. Install Python Dependencies

```bash
# Standard installation
pip install -r requirements.txt

# With dev tools (for development)
pip install -r requirements.txt pytest black flake8 mypy

# Upgrade pip first (recommended)
pip install --upgrade pip
```

**Key Dependencies:**
- `fastapi` - REST API framework
- `pydantic` - Data validation
- `sqlite3` - Profile database management
- `requests` - HTTP client
- `cryptography` - Security operations
- `psutil` - System monitoring

### 4. Verify Installation

```bash
# Check Python version
python --version          # Should be 3.10+

# Check Git
git --version             # Should be 2.30+

# Verify core modules can import
python -c "import backend.core.genesis_engine; print('✓ Core engine loaded')"
python -c "import backend.modules.commerce_injector; print('✓ Commerce module loaded')"

# Check Firefox profile directories exist
ls lucid_profile_data/    # Should list profile folders

# Verify engine folder exists
ls engine/                # Should have browser binaries

# Run self-check
python verify_readiness.py
```

### 5. Configure (Optional)

**Python Path (if not added to PATH):**
```bash
# Linux/macOS
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Windows PowerShell
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
```

**Git Hooks (auto-setup on future clones):**
```bash
git config core.hooksPath .githooks
```

---

## Verification

### Minimal Verification (2 minutes)

```bash
# 1. Check main entry point
python main.py --help

# 2. Check API can start
timeout 5 python -m uvicorn backend.lucid_api:app --host 127.0.0.1 --port 8000 2>/dev/null || echo "API ready"

# 3. Check profile data
ls -la lucid_profile_data/ | head -5
```

### Full Verification (5 minutes)

```bash
# Run built-in verification script
python verify_readiness.py

# Expected output:
# ✓ Python environment OK
# ✓ Dependencies installed
# ✓ Core modules loadable
# ✓ Profile directories exist
# ✓ Database files accessible
# ✓ Firefox binary found
# ✓ All checks passed!
```

### Profile-Specific Verification

```bash
# Check Titan profiles
python -c "
import os
profiles = [d for d in os.listdir('lucid_profile_data') if d.startswith('Titan_')]
for profile in profiles:
    print(f'✓ {profile}')
"

# Verify profile databases
python -c "
import sqlite3
import os
for profile in os.listdir('lucid_profile_data'):
    profile_path = f'lucid_profile_data/{profile}'
    if os.path.isdir(profile_path):
        db_file = f'{profile_path}/cookies.sqlite'
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM moz_cookies')
                count = cursor.fetchone()[0]
                print(f'✓ {profile}: {count} cookies')
                conn.close()
            except Exception as e:
                print(f'✗ {profile}: {e}')
"
```

---

## Docker Installation (Optional)

For containerized deployment:

```bash
# Build Docker image
docker build -t lucid-empire:latest .

# Run container (interactive)
docker run -it --rm -p 8000:8000 lucid-empire:latest

# Run with volume mount (persistent data)
docker run -it --rm -v $(pwd)/lucid_profile_data:/app/lucid_profile_data \
  -p 8000:8000 lucid-empire:latest

# Run API in background
docker run -d --name lucid-api -p 8000:8000 lucid-empire:latest
docker logs -f lucid-api
```

**Dockerfile** is included in repository root.

---

## Troubleshooting

### Common Issues

#### 1. "Python 3.10+ not found"

**Windows:**
```powershell
# Download from https://www.python.org/downloads/
# During install, ENSURE "Add Python to PATH" is checked

# Verify
python --version   # Should show 3.10+
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.11
# Or download from https://www.python.org/downloads/
```

---

#### 2. "setup_externals.sh: Permission denied"

```bash
# Fix permissions
chmod +x setup_externals.sh
./setup_externals.sh
```

---

#### 3. "PowerShell script cannot be loaded"

```powershell
# Allow execution for current session only
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Then run
.\setup_externals.ps1

# To allow permanently (not recommended for security)
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

#### 4. "curl/wget not found"

**Windows:**
```powershell
# Use built-in PowerShell download
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri "https://github.com/.../releases/.../engine.tar.gz" -OutFile engine.tar.gz

# Or install curl via winget
winget install curl
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install curl wget

# Fedora/RHEL
sudo dnf install curl wget
```

**macOS:**
```bash
# Already included, or via Homebrew
brew install curl wget
```

---

#### 5. "tar: Command not found"

**Windows PowerShell:**
```powershell
# Use PowerShell's built-in extraction
Expand-Archive -Path engine.tar.gz -DestinationPath .
```

**Linux (if minimal install):**
```bash
sudo apt install tar  # or: sudo dnf install tar
```

---

#### 6. "ModuleNotFoundError: No module named 'backend'"

```bash
# Ensure you're in repository root
cd lucid-empire-new

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
# OR
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"  # PowerShell

# Try again
python -c "import backend.core.genesis_engine"
```

---

#### 7. "Pip install fails with permission error"

```bash
# Use user flag
pip install --user -r requirements.txt

# OR use venv (recommended)
python -m venv venv
source venv/bin/activate      # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1   # Windows PowerShell

# Then install
pip install -r requirements.txt
```

---

#### 8. "Network timeout during download"

```bash
# Increase timeout and set retry
pip install --default-timeout=1000 -r requirements.txt

# Or download manually from:
# https://github.com/malithwishwa02-dot/lucid-empire-new/releases

# Extract manually:
tar -xzf engine.tar.gz
tar -xzf bin.tar.gz
```

---

#### 9. "sqlite3 database is locked"

```bash
# Close other processes using profile data
# Then delete lock files
rm -f lucid_profile_data/*/cookies.sqlite-lock
rm -f lucid_profile_data/*/places.sqlite-lock

# Retry operation
```

---

### Getting Help

1. **Check existing docs:**
   - `USAGE_GUIDE.md` - How to use features
   - `API_REFERENCE.md` - API documentation
   - `TROUBLESHOOTING.md` - Extended troubleshooting

2. **Verify installation:**
   ```bash
   python verify_readiness.py  # Comprehensive check
   ```

3. **Check logs:**
   ```bash
   # If you've run the system, check recent logs
   tail -100 lucid_*.log 2>/dev/null || echo "No logs yet"
   ```

4. **Report issues:**
   - GitHub Issues: https://github.com/malithwishwa02-dot/lucid-empire-new/issues
   - Include: OS, Python version, Git version, error message

---

## Next Steps

✅ Installation complete!

1. **Read the Usage Guide:** `USAGE_GUIDE.md`
2. **Understand the API:** `API_REFERENCE.md`
3. **Check Examples:** See `scripts/` folder
4. **Run a Test:** `python scripts/simulate_missions.py`

---

## References

- **Official Repo:** https://github.com/malithwishwa02-dot/lucid-empire-new
- **Python:** https://www.python.org/
- **Firefox:** https://www.mozilla.org/firefox/
- **Git:** https://git-scm.com/

---

**Last Updated:** February 2, 2026  
**Version:** 1.0.0
