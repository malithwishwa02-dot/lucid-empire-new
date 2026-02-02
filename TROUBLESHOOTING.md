# Lucid Empire - Troubleshooting Guide

Comprehensive troubleshooting for common issues and their solutions.

## Quick Diagnosis

Run the automated health check first:
```bash
python verify_readiness.py
```

If that doesn't pinpoint the issue, use this guide.

---

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [API Issues](#api-issues)
3. [Browser Issues](#browser-issues)
4. [Profile Issues](#profile-issues)
5. [Database Issues](#database-issues)
6. [Performance Issues](#performance-issues)
7. [Network/Proxy Issues](#networkproxy-issues)
8. [Getting Help](#getting-help)

---

## Installation Issues

### "Python 3.10+ not found"

**Symptom:** Error when running `python` or `python3`

**Solution:**

**Windows:**
1. Download Python 3.11 from https://www.python.org/downloads/
2. **IMPORTANT:** During installation, check "Add Python to PATH"
3. Restart terminal/IDE
4. Verify: `python --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3.11 python3.11-devel
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Or download from https://www.python.org/downloads/
```

---

### "Permission denied" for setup_externals.sh

**Symptom:**
```
bash: ./setup_externals.sh: Permission denied
```

**Solution:**
```bash
chmod +x setup_externals.sh
./setup_externals.sh
```

**On WSL/Git Bash, may also need:**
```bash
git config core.fileMode false
chmod +x setup_externals.sh
./setup_externals.sh
```

---

### "PowerShell script cannot be loaded"

**Symptom:**
```
File cannot be loaded because running scripts is disabled on this system
```

**Solution (Current Session Only):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup_externals.ps1
```

**Solution (Permanent - Not Recommended):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Then run:**
```powershell
.\setup_externals.ps1
```

---

### "ModuleNotFoundError: No module named 'backend'"

**Symptom:**
```
ModuleNotFoundError: No module named 'backend'
```

**Cause:** Not in repository root directory

**Solution:**
```bash
# Verify you're in correct directory
pwd  # Should end with: lucid-empire-new

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS

# Windows PowerShell
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"

# Try again
python -c "import backend.core.genesis_engine; print('✓ OK')"
```

---

### "pip install fails with permission error"

**Symptom:**
```
ERROR: Could not install packages due to a PermissionError
```

**Solution 1 (Recommended - Use Virtual Environment):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows PowerShell

pip install -r requirements.txt
```

**Solution 2 (User Install):**
```bash
pip install --user -r requirements.txt
```

**Solution 3 (Use sudo - Not Recommended):**
```bash
sudo pip install -r requirements.txt
```

---

### "curl/wget not found"

**Symptom:**
```
curl: command not found
wget: command not found
```

**Solution:**

**Windows PowerShell:**
```powershell
# If using Windows 10+, curl is built-in
# Try: curl --version

# If not available, install via winget:
winget install curl
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install curl wget
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install curl wget
```

**macOS:**
```bash
brew install curl wget
```

---

### "tar: Command not found"

**Symptom:**
```
'tar' is not recognized as an internal or external command
```

**Solution (Windows PowerShell):**
```powershell
# Use PowerShell's built-in extraction
Expand-Archive -Path engine.tar.gz -DestinationPath .
Expand-Archive -Path bin.tar.gz -DestinationPath .
```

**Solution (Linux):**
```bash
sudo apt install tar  # Ubuntu/Debian
# OR
sudo dnf install tar  # Fedora/RHEL
```

---

### "Network timeout during download"

**Symptom:**
```
ConnectionError: Connection timed out
```

**Solution:**
```bash
# Increase timeout
export PIP_DEFAULT_TIMEOUT=1000
pip install -r requirements.txt

# Or download setup files manually:
# 1. Visit: https://github.com/malithwishwa02-dot/lucid-empire-new/releases
# 2. Download engine.tar.gz and bin.tar.gz
# 3. Extract manually:
tar -xzf engine.tar.gz
tar -xzf bin.tar.gz
```

---

## API Issues

### "Address already in use" (Port 8000)

**Symptom:**
```
ERROR: Address already in use: ('0.0.0.0', 8000)
```

**Solution 1 (Use Different Port):**
```bash
python -m uvicorn backend.lucid_api:app --port 8001
```

**Solution 2 (Kill Process Using Port):**

**Linux/macOS:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Windows PowerShell:**
```powershell
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

---

### "No module named 'fastapi'"

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn pydantic
```

---

### "API responds with 500 error"

**Symptom:**
```json
{"detail": "Internal server error"}
```

**Diagnosis:**
```bash
# Check API logs
tail -50 logs/lucid-api.log | grep -i error

# Run with debug output
python -m uvicorn backend.lucid_api:app --log-level debug
```

**Common Causes & Solutions:**
1. Profile not found → Verify profile name exists: `ls lucid_profile_data/`
2. Database locked → See [Database Issues](#database-issues)
3. Firefox not found → See [Browser Issues](#browser-issues)
4. Insufficient permissions → Check directory ownership

---

### "CORS error in browser"

**Symptom:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution (Add to lucid_api.py):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Browser Issues

### "Firefox won't launch"

**Symptom:**
```
FileNotFoundError: firefox binary not found
```

**Solution:**

**Step 1: Verify Firefox binary exists**
```bash
ls -la engine/firefox/firefox
# If not found, download it:
./setup_externals.sh  # or .\setup_externals.ps1
```

**Step 2: Check permissions**
```bash
chmod +x engine/firefox/firefox
```

**Step 3: Test Firefox directly**
```bash
./engine/firefox/firefox --version
# Should print: Mozilla Firefox 147.0
```

**Step 4: Try launching with verbose output**
```bash
python lucid_launcher.py --profile Titan_SoftwareEng_USA_001 --verbose 2>&1 | head -50
```

---

### "Firefox crashes immediately"

**Symptom:**
```
Process exited with code 1
```

**Causes & Solutions:**

**1. Corrupted profile directory:**
```bash
# Backup and delete profile cache
mv lucid_profile_data/Titan_SoftwareEng_USA_001/cache old_cache/
rm -rf lucid_profile_data/Titan_SoftwareEng_USA_001/cache

# Retry
./engine/firefox/firefox -profile lucid_profile_data/Titan_SoftwareEng_USA_001
```

**2. Missing extensions:**
```bash
# Check extensions directory
ls lucid_profile_data/Titan_SoftwareEng_USA_001/extensions/

# If empty, reinstall:
# See backend/modules/browser_setup.py
```

**3. Incompatible prefs.js:**
```bash
# Backup and reset
cp lucid_profile_data/Titan_SoftwareEng_USA_001/prefs.js \
   lucid_profile_data/Titan_SoftwareEng_USA_001/prefs.js.bak

# Generate default prefs
python -c "
from backend.core.genesis_engine import ProfileFactory
factory = ProfileFactory()
factory.regenerate_prefs('Titan_SoftwareEng_USA_001')
"
```

---

### "Firefox window won't close"

**Symptom:**
```
Browser stays open after timeout
```

**Solution:**
```bash
# Kill all Firefox processes
pkill -f firefox  # Linux/macOS
taskkill /IM firefox.exe /F  # Windows

# Or kill specific PID
kill -9 <PID>

# Check if killed
ps aux | grep firefox | grep -v grep
```

---

## Profile Issues

### "Profile not found"

**Symptom:**
```
Error: Profile 'Nonexistent_Profile' not found
```

**Solution:**
```bash
# List available profiles
ls lucid_profile_data/

# Or via API
curl http://localhost:8000/profiles | jq .

# Create new profile
curl -X POST http://localhost:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New_Profile",
    "identity": {"first_name": "John", "last_name": "Doe"},
    "payment": {"card_number": "4111111111111111", "cvv": "123"}
  }'
```

---

### "Profile creation fails"

**Symptom:**
```
Error: Profile already exists
```

**Solution:**
Use a different profile name or delete the existing one:

```bash
# Delete existing profile
rm -rf lucid_profile_data/Titan_SoftwareEng_USA_001

# Then create new one
python -c "
from backend.core.genesis_engine import ProfileFactory
factory = ProfileFactory()
factory.create_profile({
    'name': 'Titan_SoftwareEng_USA_001',
    'identity': {...}
})
"
```

---

### "Profile data corrupted"

**Symptom:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solution:**
```bash
# 1. Check integrity
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/cookies.sqlite \
  "PRAGMA integrity_check;"

# 2. If corrupted, restore from backup
tar -xzf backups/lucid_backup_20260201.tar.gz lucid_profile_data/Titan_SoftwareEng_USA_001

# 3. Or recreate profile
rm -rf lucid_profile_data/Titan_SoftwareEng_USA_001
python forge_multi_profile.py
```

---

## Database Issues

### "Database is locked"

**Symptom:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**

**1. Find what's holding the lock:**
```bash
lsof lucid_profile_data/*/cookies.sqlite
```

**2. Kill the process:**
```bash
kill -9 <PID>
```

**3. Remove lock files:**
```bash
rm -f lucid_profile_data/*/cookies.sqlite-lock
rm -f lucid_profile_data/*/cookies.sqlite-journal
rm -f lucid_profile_data/*/places.sqlite-lock
rm -f lucid_profile_data/*/places.sqlite-journal
```

**4. Verify database integrity:**
```bash
sqlite3 lucid_profile_data/*/cookies.sqlite "PRAGMA integrity_check;"
```

---

### "Database is read-only"

**Symptom:**
```
sqlite3.OperationalError: attempt to write a readonly database
```

**Solution:**

**1. Check file permissions:**
```bash
ls -la lucid_profile_data/Titan_SoftwareEng_USA_001/
```

**2. Fix permissions:**
```bash
chmod 755 lucid_profile_data/Titan_SoftwareEng_USA_001/
chmod 644 lucid_profile_data/Titan_SoftwareEng_USA_001/*.sqlite
```

**3. Check directory ownership (if using sudo):**
```bash
sudo chown -R $USER:$USER lucid_profile_data/
```

---

### "Database query too slow"

**Symptom:**
```
Query takes more than 5 seconds
```

**Solution:**

**1. Optimize database:**
```bash
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/places.sqlite \
  "VACUUM; ANALYZE;"
```

**2. Create indexes:**
```bash
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/places.sqlite <<EOF
CREATE INDEX IF NOT EXISTS idx_visits_date ON moz_historyvisits(visit_date DESC);
CREATE INDEX IF NOT EXISTS idx_places_id ON moz_places(id);
ANALYZE;
EOF
```

**3. Check table sizes:**
```bash
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/places.sqlite \
  "SELECT name, COUNT(*) FROM (SELECT 'history' AS name FROM moz_historyvisits UNION ALL SELECT 'places' FROM moz_places) GROUP BY name;"
```

---

## Performance Issues

### "High CPU usage"

**Symptom:**
```
Python process using 80%+ CPU
```

**Diagnosis:**
```bash
# Find which process
top -b -n 1 | head -20

# Which Firefox?
ps aux | grep firefox

# Which Python function?
python -m cProfile main.py 2>&1 | head -50
```

**Solutions:**

**1. Too many browser instances:**
```bash
ps aux | grep firefox | wc -l
pkill -f firefox  # Kill all
```

**2. Infinite loop in code:**
```bash
# Check for processes in D state (uninterruptible)
ps aux | grep " D "
kill -9 <PID>
```

**3. Database query optimization:**
See [Database Issues](#database-issues)

---

### "High memory usage"

**Symptom:**
```
Memory usage grows over time
```

**Diagnosis:**
```bash
# Check memory per process
ps aux --sort=-%mem | head -10

# Monitor Firefox memory
watch -n 1 "ps aux | grep firefox | grep -v grep"

# Check for memory leaks
python -m memory_profiler main.py
```

**Solutions:**

**1. Kill old Firefox processes:**
```bash
# Find processes older than 1 hour
ps aux | grep firefox | awk '{if ($9 > "01:00") print $2}' | xargs kill -9
```

**2. Enable garbage collection:**
```python
import gc
gc.collect()
gc.set_threshold(1000, 10, 10)
```

**3. Use tmpfs for temporary files:**
```bash
mount -t tmpfs -o size=1G tmpfs /mnt/ramdisk
export TMPDIR=/mnt/ramdisk
```

---

### "Slow API response"

**Symptom:**
```
API endpoint takes >5 seconds
```

**Diagnosis:**
```bash
# Measure response time
time curl http://localhost:8000/profiles

# Check API logs for slow queries
grep "duration" logs/lucid-api.log | sort -t: -k2 -rn | head -10
```

**Solutions:**

**1. Add caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_profile(name):
    # ... fetch profile
```

**2. Use async operations:**
```python
@app.get("/profiles")
async def list_profiles():
    # Use async database calls
    profiles = await db.fetch_profiles()
    return profiles
```

**3. Add database indexes:**
See [Database Issues](#database-issues)

---

## Network/Proxy Issues

### "Cannot connect to proxy"

**Symptom:**
```
ProxyError: Unable to connect to proxy
```

**Solution:**

**1. Verify proxy is accessible:**
```python
import socket

proxy_host = "192.168.1.50"
proxy_port = 1080

try:
    socket.create_connection((proxy_host, proxy_port), timeout=5)
    print(f"✓ Proxy {proxy_host}:{proxy_port} is reachable")
except:
    print(f"✗ Cannot reach proxy {proxy_host}:{proxy_port}")
```

**2. Check proxy credentials:**
```python
from backend.network.proxy_manager import ProxyManager

manager = ProxyManager()
proxy = manager.get_proxy('Titan_SoftwareEng_USA_001')
print(f"Proxy: {proxy['type']}://{proxy['username']}:***@{proxy['host']}:{proxy['port']}")
```

**3. Test with curl:**
```bash
curl --socks5 user:pass@192.168.1.50:1080 https://www.example.com
```

---

### "Proxy authentication failed"

**Symptom:**
```
Proxy authentication failed
```

**Solution:**

**1. Verify credentials:**
```bash
# Check in profile
cat lucid_profile_data/Titan_SoftwareEng_USA_001/prefs.js | grep proxy
```

**2. Update credentials:**
```python
from backend.core.genesis_engine import ProfileFactory

factory = ProfileFactory()
factory.update_profile('Titan_SoftwareEng_USA_001', {
    'proxy': {
        'username': 'correct_username',
        'password': 'correct_password'
    }
})
```

**3. Test credentials manually:**
```bash
curl --socks5 newuser:newpass@192.168.1.50:1080 -v https://www.example.com 2>&1 | grep -i proxy
```

---

### "Network timeout"

**Symptom:**
```
ConnectionError: Network is unreachable
```

**Solution:**

**1. Check network connectivity:**
```bash
ping 8.8.8.8  # Google DNS
curl -I https://www.example.com
```

**2. Check if proxy is timing out:**
```bash
timeout 10 curl --socks5 user:pass@proxy:1080 https://www.example.com -v
```

**3. Increase timeout:**
```python
from backend.network.proxy_manager import ProxyManager

manager = ProxyManager()
manager.timeout = 60  # 60 seconds
```

---

## Getting Help

### Collect Diagnostic Information

```bash
#!/bin/bash
# Create diagnostic bundle

echo "=== System Info ===" > diagnostics.txt
uname -a >> diagnostics.txt
python --version >> diagnostics.txt
git --version >> diagnostics.txt

echo -e "\n=== Verification ===" >> diagnostics.txt
python verify_readiness.py >> diagnostics.txt 2>&1

echo -e "\n=== API Health ===" >> diagnostics.txt
curl -s http://localhost:8000/health >> diagnostics.txt 2>&1

echo -e "\n=== Recent Errors ===" >> diagnostics.txt
grep ERROR logs/lucid-api.log | tail -20 >> diagnostics.txt 2>/dev/null

echo -e "\n=== Process Status ===" >> diagnostics.txt
ps aux | grep -E "(firefox|python|lucid)" >> diagnostics.txt

echo "✓ Diagnostic information saved to: diagnostics.txt"
```

### Create Issue on GitHub

When reporting an issue, include:
1. Operating System (Windows 10, Ubuntu 20.04, macOS 12, etc.)
2. Python version: `python --version`
3. Git version: `git --version`
4. Error message (full traceback if available)
5. Steps to reproduce
6. Output from `python verify_readiness.py`

**Report at:** https://github.com/malithwishwa02-dot/lucid-empire-new/issues

### Contact Support

- **Email:** support@example.com
- **Discord:** [Link to Discord server]
- **Documentation:** Read INSTALLATION.md, USAGE_GUIDE.md, API_REFERENCE.md

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Port 8000 in use | `python -m uvicorn backend.lucid_api:app --port 8001` |
| Firefox won't launch | `./setup_externals.sh` |
| Profile not found | `ls lucid_profile_data/` |
| Database locked | `rm -f lucid_profile_data/*/cookies.sqlite-lock` |
| High memory | `pkill -f firefox` |
| Slow API | Check logs: `tail -f logs/lucid-api.log` |
| Python import error | `export PYTHONPATH="${PYTHONPATH}:$(pwd)"` |
| Permission denied | `chmod +x setup_externals.sh` |

---

**Last Updated:** February 2, 2026  
**Version:** 1.0.0
