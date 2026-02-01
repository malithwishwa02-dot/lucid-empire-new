#!/bin/bash
# LUCID EMPIRE :: Post-Clone Binary Restoration
# Automatically restores binary files from bundle after git clone
# Platform: Linux/macOS
# Usage: After cloning, run: ./setup-binaries.sh

set -e

echo "[LUCID] Post-Clone Binary Setup for Linux/macOS"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[*] Repository path: $REPO_DIR"

# Configuration
BUNDLE_NAME="lucid-11commits.bundle.zip"
BUNDLE_URL="https://github.com/malithwishwa02-dot/lucid-empire-new/releases/download/v5.0-binaries/${BUNDLE_NAME}"
BACKUP_BUNDLE="/tmp/${BUNDLE_NAME}"
TEMP_EXTRACT="/tmp/lucid-bundle-extract"

# Function to download bundle
download_bundle() {
    echo -e "${YELLOW}[!] Binary files not found. Downloading bundle...${NC}"
    
    if command -v curl &> /dev/null; then
        curl -L -o "$BACKUP_BUNDLE" "$BUNDLE_URL"
    elif command -v wget &> /dev/null; then
        wget -O "$BACKUP_BUNDLE" "$BUNDLE_URL"
    else
        echo -e "${RED}[ERROR] Neither curl nor wget found. Cannot download bundle.${NC}"
        echo "Please download manually from: $BUNDLE_URL"
        exit 1
    fi
    
    if [ ! -f "$BACKUP_BUNDLE" ]; then
        echo -e "${RED}[ERROR] Failed to download bundle${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Bundle downloaded successfully${NC}"
}

# Function to extract bundle
extract_bundle() {
    echo -e "${YELLOW}[!] Extracting bundle (this may take a moment)...${NC}"
    
    mkdir -p "$TEMP_EXTRACT"
    
    if [[ "$BACKUP_BUNDLE" == *.zip ]]; then
        if command -v unzip &> /dev/null; then
            unzip -q "$BACKUP_BUNDLE" -d "$TEMP_EXTRACT"
        else
            echo -e "${RED}[ERROR] unzip not found${NC}"
            exit 1
        fi
    else
        tar -xzf "$BACKUP_BUNDLE" -C "$TEMP_EXTRACT"
    fi
    
    echo -e "${GREEN}[+] Bundle extracted${NC}"
}

# Function to restore git objects
restore_git_objects() {
    echo -e "${YELLOW}[!] Restoring git objects and binary files...${NC}"
    
    cd "$TEMP_EXTRACT"
    
    # Bundle contains all git history
    git bundle verify "lucid-11commits.bundle" > /dev/null 2>&1 || {
        echo -e "${RED}[ERROR] Bundle verification failed${NC}"
        exit 1
    }
    
    # Fetch from bundle into current repo
    cd "$REPO_DIR"
    git fetch "$TEMP_EXTRACT/lucid-11commits.bundle" refs/heads/main:refs/remotes/bundle/main
    
    echo -e "${GREEN}[+] Git objects restored${NC}"
}

# Function to verify restoration
verify_restoration() {
    echo -e "${YELLOW}[!] Verifying binary files...${NC}"
    
    files_to_check=(
        "camoufox/.gitkeep_placeholder"
        "assets/.gitkeep_placeholder"
        "engine/.gitkeep_placeholder"
        "lucid_profile_data/.gitkeep_placeholder"
        "packaging/.gitkeep_placeholder"
        "research_reports/.gitkeep_placeholder"
        "backend/core/genesis_engine.py"
        "backend/modules/commerce_injector.py"
        "backend/network/xdp_outbound.c"
    )
    
    missing=0
    for file in "${files_to_check[@]}"; do
        if [ -f "$REPO_DIR/$file" ]; then
            echo -e "${GREEN}[✓]${NC} $file"
        else
            echo -e "${RED}[✗]${NC} $file (missing)"
            ((missing++))
        fi
    done
    
    if [ $missing -eq 0 ]; then
        echo -e "${GREEN}[+] All files verified successfully!${NC}"
        return 0
    else
        echo -e "${RED}[!] $missing files missing${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo ""
    
    # Check if binaries already exist
    if [ -f "$REPO_DIR/camoufox/.gitkeep_placeholder" ] && \
       [ -f "$REPO_DIR/backend/core/genesis_engine.py" ]; then
        echo -e "${GREEN}[+] Binary files already present!${NC}"
        verify_restoration
        exit 0
    fi
    
    # Check for local bundle backup
    if [ -f "$BACKUP_BUNDLE" ]; then
        echo -e "${GREEN}[+] Found local bundle backup${NC}"
    else
        download_bundle
    fi
    
    extract_bundle
    restore_git_objects
    verify_restoration
    
    # Cleanup
    echo -e "${YELLOW}[*] Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_EXTRACT"
    
    echo ""
    echo -e "${GREEN}[SUCCESS] Binary restoration complete!${NC}"
    echo -e "${GREEN}[+] Repository is now fully functional${NC}"
    echo ""
}

main "$@"
