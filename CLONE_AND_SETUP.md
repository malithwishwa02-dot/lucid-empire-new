# Clone & Setup Guide for Lucid Empire

## Automatic Binary Restoration on Clone

When someone clones this repository, binary files are automatically restored using intelligent setup scripts.

## ⚡ Quick Start (All Platforms)

### **Option 1: Enable Auto-Restore (Recommended)**

After cloning, enable git hooks for automatic restoration:

```bash
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new

# Enable automatic post-clone hook
git config core.hooksPath .githooks

# For future clones, this will run automatically
```

### **Option 2: Manual Setup (All Platforms)

**Linux/macOS:**
```bash
cd lucid-empire-new
chmod +x setup-binaries.sh
./setup-binaries.sh
```

**Windows (PowerShell):**
```powershell
cd lucid-empire-new
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup-binaries.ps1
```

## 🔧 How It Works

### **Clone Process**
```
1. git clone <repo>
   ↓
2. .githooks/post-clone hook detected
   ↓
3. Automatically runs setup-binaries script
   ↓
4. Binary files restored from bundle
   ↓
5. Repository fully functional
```

### **Manual Process**
```
1. git clone <repo>
   ↓
2. Run setup-binaries.sh (or .ps1)
   ↓
3. Script checks for missing files
   ↓
4. Downloads bundle from GitHub Releases (if needed)
   ↓
5. Extracts and restores all binary files
   ↓
6. Verifies installation
```

## 📦 What Gets Restored

The setup scripts restore:

✅ **Backend Code** (already in repo)
- `backend/core/` - Profile factory, temporal displacement, core engine
- `backend/modules/` - Behavioral simulation, commerce injection
- `backend/network/` - eBPF/XDP kernel integration

✅ **Directory Placeholders** (descriptive structure)
- `camoufox/` - Browser library structure documentation
- `assets/` - Configuration files and templates
- `engine/` - Browser engine binary placeholders
- `lucid_profile_data/` - Profile storage structure
- `packaging/` - Distribution artifacts directory
- `research_reports/` - Analysis reports structure

✅ **Documentation** (all .md files)
- Setup guides
- Technical specifications
- API documentation

## 🌍 Network Handling

### **Smart Download**
The scripts intelligently handle network conditions:

```bash
# Automatic detection
- Checks if binaries already exist → Skip download
- Tries curl first → Falls back to wget
- On Windows uses built-in WebClient
- Provides manual download link if all else fails
```

### **Slow Network (100 kbps)
**Option A: Automatic**
```bash
# Scripts will download ~229 MB compressed
# Estimated time: 30-45 minutes
chmod +x setup-binaries.sh
./setup-binaries.sh
```

**Option B: Local Transfer**
```bash
# Copy bundle locally first
cp /local/path/lucid-11commits.bundle.zip .

# Run setup with local bundle
BUNDLE_PATH=./lucid-11commits.bundle.zip ./setup-binaries.sh
```

**Option C: USB/Cloud Storage**
```bash
# Transfer bundle via USB or cloud (faster for slow networks)
# Then use local option above
```

## ⚙️ Configuration

### **Environment Variables (Linux/macOS)**

```bash
# Use local bundle instead of downloading
export BUNDLE_PATH="/path/to/bundle.zip"
chmod +x setup-binaries.sh
./setup-binaries.sh

# Custom download URL
export BUNDLE_URL="https://custom-mirror.com/bundle.zip"
./setup-binaries.sh
```

### **PowerShell Parameters (Windows)**

```powershell
# Use local bundle
.\setup-binaries.ps1 -UseLocalBundle -LocalBundlePath "C:\path\to\bundle.zip"

# Custom download URL
.\setup-binaries.ps1 -BundleUrl "https://custom-mirror.com/bundle.zip"
```

## 🐛 Troubleshooting

### **Issue: "Permission denied" (Linux/macOS)**
**Solution:**
```bash
chmod +x setup-binaries.sh
./setup-binaries.sh
```

### **Issue: "cannot be loaded" (PowerShell Windows)**
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup-binaries.ps1
```

### **Issue: "Bundle download failed"**
**Solution:**
1. Check internet connection
2. Download manually from GitHub Releases
3. Place in repository directory
4. Run: `./setup-binaries.sh -UseLocalBundle`

### **Issue: "Insufficient disk space"**
**Requirements:**
- Bundle (compressed): 229 MB
- Temporary extraction: 600 MB
- Final installation: 1.1 GB
- **Total needed: 2 GB minimum**

**Solution:** Free up disk space or use cloud storage alternative

### **Issue: "Git bundle verification failed"**
**Solution:**
```bash
# Manually verify and restore
git bundle verify lucid-11commits.bundle
git fetch lucid-11commits.bundle refs/heads/*:refs/remotes/bundle/*
```

## 🚀 CI/CD Integration

### **GitHub Actions**
```yaml
name: Build with Lucid Empire
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Restore binaries
        run: |
          chmod +x setup-binaries.sh
          ./setup-binaries.sh
      - name: Run tests
        run: make test
```

### **GitLab CI**
```yaml
build:
  script:
    - chmod +x setup-binaries.sh
    - ./setup-binaries.sh
    - make build
```

### **Jenkins**
```groovy
stage('Setup') {
    steps {
        sh 'chmod +x setup-binaries.sh'
        sh './setup-binaries.sh'
    }
}
```

## 📋 File Structure After Setup

```
lucid-empire-new/
├── .github/                    # GitHub actions
├── .githooks/                  # Git hooks (auto-restore)
├── backend/                    # Core modules
│   ├── core/                   # Profile factory, engines
│   ├── modules/                # Behavioral simulation
│   └── network/                # eBPF/XDP integration
├── camoufox/                   # Browser library (placeholder)
├── assets/                     # Configs and templates
├── engine/                     # Browser engines (placeholder)
├── lucid_profile_data/         # Profile storage (placeholder)
├── packaging/                  # Distributions (placeholder)
├── research_reports/           # Analysis reports (placeholder)
├── setup-binaries.sh          # Linux/macOS setup
├── setup-binaries.ps1         # Windows setup
├── SETUP_BINARIES_README.md   # Setup documentation
├── CLONE_AND_SETUP.md         # This file
├── .gitattributes             # Binary file handling
├── README.md                  # Main documentation
└── ...
```

## ✅ Verification

After setup completes, verify installation:

```bash
# Check core backend files
ls backend/core/genesis_engine.py
ls backend/modules/commerce_injector.py
ls backend/network/xdp_outbound.c

# Check placeholders
ls camoufox/.gitkeep_placeholder
ls assets/.gitkeep_placeholder

# List all restored files
git ls-tree -r HEAD | head -20
```

## 📞 Support

If issues persist:
1. Review the troubleshooting section
2. Check script output for specific errors
3. Open GitHub issue with:
   - Operating system
   - Git version: `git --version`
   - Error message (full output)
   - Network type (wired/wireless/mobile)

## 🔐 Security Notes

- Scripts only download from official GitHub Releases
- Bundle is git-verified before restoration
- No external credentials or tokens required
- All operations logged to console
- Safe to run multiple times (idempotent)

## ⏱️ Expected Times

| Speed | Download Time | Extract | Setup Total |
|-------|---------------|---------|-------------|
| 10 Mbps | ~3 minutes | ~2 min | ~5 min |
| 1 Mbps | ~30 minutes | ~2 min | ~32 min |
| 100 kbps | ~5 hours | ~2 min | ~5h 2min |
| USB/Local | ~0 min | ~2 min | ~2 min |

**Recommendation for slow networks:** Use USB or cloud storage transfer instead of downloading.
