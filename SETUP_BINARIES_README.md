# Post-Clone Automatic Setup

When someone clones this repository, they need to restore the binary files from the bundle. This directory contains setup scripts for both platforms.

## Quick Start

### **Linux/macOS**
```bash
cd lucid-empire-new
chmod +x setup-binaries.sh
./setup-binaries.sh
```

### **Windows (PowerShell)**
```powershell
cd lucid-empire-new
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\setup-binaries.ps1
```

## What These Scripts Do

1. **Check Prerequisites**
   - Verify Git is installed
   - Check for compression tools (7-Zip, unzip, or built-in)

2. **Detect Missing Files**
   - Test if binary files are already present
   - If missing, proceed with download and restoration

3. **Download Bundle**
   - Fetch `lucid-11commits.bundle.zip` from GitHub Releases
   - Uses curl (Linux/macOS) or PowerShell WebClient (Windows)
   - Falls back to manual download instructions if needed

4. **Extract & Restore**
   - Decompress the bundle
   - Run `git bundle verify` to validate integrity
   - Restore all git objects and binary files

5. **Verify Installation**
   - Check all critical files are present
   - Verify file integrity
   - Report success or issues

## Manual Alternative

If scripts fail, manually restore:

```bash
# Download from GitHub Releases
wget https://github.com/malithwishwa02-dot/lucid-empire-new/releases/download/v5.0-binaries/lucid-11commits.bundle.zip

# Extract
unzip lucid-11commits.bundle.zip

# Restore to git
git fetch lucid-11commits.bundle refs/heads/main:refs/remotes/bundle/main
```

## Environment Variables (Linux/macOS)

```bash
# Use local bundle instead of downloading
BUNDLE_PATH=/path/to/lucid-11commits.bundle.zip ./setup-binaries.sh

# Specify custom download URL
BUNDLE_URL=https://custom-url/bundle.zip ./setup-binaries.sh
```

## PowerShell Parameters

```powershell
# Use local bundle
.\setup-binaries.ps1 -UseLocalBundle -LocalBundlePath "C:\path\to\bundle.zip"

# Use custom download URL
.\setup-binaries.ps1 -BundleUrl "https://custom-url/bundle.zip"
```

## Troubleshooting

### Script Permission Denied (Linux/macOS)
```bash
chmod +x setup-binaries.sh
```

### PowerShell Execution Policy (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Network Issues
- Check internet connection
- Verify GitHub Releases are accessible
- Download bundle manually from releases page

### Disk Space
- Bundle: ~229 MB (compressed)
- Extracted: ~600 MB (temporary)
- Final installation: ~1.1 GB
- Ensure you have at least 2 GB free

## CI/CD Integration

### GitHub Actions
```yaml
- name: Restore binary files
  run: |
    chmod +x setup-binaries.sh
    ./setup-binaries.sh
```

### GitLab CI
```yaml
setup_binaries:
  script:
    - chmod +x setup-binaries.sh
    - ./setup-binaries.sh
```

### Jenkins
```groovy
sh 'chmod +x setup-binaries.sh'
sh './setup-binaries.sh'
```

## Files Restored

After running the setup script, you'll have:

✅ **Core Modules** (`backend/core/`)
- genesis_engine.py
- profile_store.py
- biometric_mimicry.py
- and 5+ more

✅ **Binary Placeholders** (directories with descriptions)
- camoufox/ (browser library structure)
- assets/ (configuration files)
- engine/ (browser engine binaries)
- lucid_profile_data/ (profile storage)
- packaging/ (distribution artifacts)
- research_reports/ (analysis data)

✅ **Documentation** (all .md files)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the script output for specific errors
3. Open an issue on GitHub with the error message
4. Provide your OS and git version: `git --version`
