#!/bin/bash
# setup_externals.sh
# Downloads and extracts external dependencies (engine/, bin/) after cloning Lucid Empire
# Usage: ./setup_externals.sh [--version latest] [--force]

set -e

# Configuration
REPO_OWNER="malithwishwa02-dot"
REPO_NAME="lucid-empire-new"
GITHUB_API="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME"
DOWNLOAD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${DOWNLOAD_DIR}/.externals_temp"
RELEASE_VERSION="latest"
FORCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --version) RELEASE_VERSION="$2"; shift 2 ;;
        --force) FORCE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Color helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

write_success() { echo -e "${GREEN}✓${NC} $1"; }
write_error() { echo -e "${RED}✗${NC} $1"; }
write_info() { echo -e "${CYAN}ℹ${NC} $1"; }

# Header
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Lucid Empire - External Dependencies Setup                        ║${NC}"
echo -e "${CYAN}║  Downloading: engine/ and bin/ folders                             ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
check_prerequisites() {
    write_info "Checking prerequisites..."
    
    if ! command -v tar &> /dev/null; then
        write_error "tar utility not found. Please install tar."
        exit 1
    fi
    
    if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
        write_error "Neither curl nor wget found. Please install curl or wget."
        echo ""
        echo "Manual installation:"
        echo "1. Download engine.tar.gz from: https://github.com/$REPO_OWNER/$REPO_NAME/releases/$RELEASE_VERSION"
        echo "2. Download bin.tar.gz from: https://github.com/$REPO_OWNER/$REPO_NAME/releases/$RELEASE_VERSION"
        echo "3. Extract both to repository root:"
        echo "   tar -xzf engine.tar.gz"
        echo "   tar -xzf bin.tar.gz"
        exit 1
    fi
    
    write_success "Prerequisites verified (curl/wget and tar available)"
}

# Get release info
get_release_info() {
    write_info "Fetching release information..."
    
    if [ "$RELEASE_VERSION" = "latest" ]; then
        RELEASE_URL="$GITHUB_API/releases/latest"
    else
        RELEASE_URL="$GITHUB_API/releases/tags/$RELEASE_VERSION"
    fi
    
    local response
    if command -v curl &> /dev/null; then
        response=$(curl -s "$RELEASE_URL")
    else
        response=$(wget -q -O - "$RELEASE_URL")
    fi
    
    if echo "$response" | grep -q "Not Found"; then
        write_error "Release not found: $RELEASE_VERSION"
        exit 1
    fi
    
    echo "$response"
}

# Download file
download_file() {
    local url=$1
    local output_path=$2
    local file_name=$3
    
    write_info "Downloading $file_name..."
    
    if command -v curl &> /dev/null; then
        if ! curl -L -o "$output_path" "$url"; then
            write_error "Failed to download $file_name"
            return 1
        fi
    else
        if ! wget -O "$output_path" "$url"; then
            write_error "Failed to download $file_name"
            return 1
        fi
    fi
    
    write_success "Downloaded: $file_name"
    return 0
}

# Extract archive
extract_archive() {
    local archive_path=$1
    local destination_path=$2
    local file_name=$(basename "$archive_path")
    
    write_info "Extracting $file_name to $destination_path..."
    
    if ! tar -xzf "$archive_path" -C "$destination_path"; then
        write_error "Failed to extract $file_name"
        return 1
    fi
    
    write_success "Extracted: $file_name"
    return 0
}

# Main
main() {
    check_prerequisites
    
    # Check if already extracted
    if [[ (-d "${DOWNLOAD_DIR}/engine" || -d "${DOWNLOAD_DIR}/bin") && "$FORCE" != "true" ]]; then
        echo ""
        write_info "External folders already present:"
        [[ -d "${DOWNLOAD_DIR}/engine" ]] && echo "  ✓ engine/"
        [[ -d "${DOWNLOAD_DIR}/bin" ]] && echo "  ✓ bin/"
        echo ""
        write_info "Use --force to re-download and overwrite"
        exit 0
    fi
    
    # Create temp directory
    mkdir -p "$TEMP_DIR"
    
    # Get release info
    release_json=$(get_release_info)
    release_tag=$(echo "$release_json" | grep -o '"tag_name":"[^"]*' | head -1 | cut -d'"' -f4)
    
    if [[ -z "$release_tag" ]]; then
        write_error "Could not parse release information"
        exit 1
    fi
    
    write_success "Found release: $release_tag"
    echo ""
    
    # Extract asset URLs using grep (works across systems)
    declare -a assets=("engine.tar.gz" "bin.tar.gz")
    
    for asset_name in "${assets[@]}"; do
        # Extract download URL for this asset
        asset_url=$(echo "$release_json" | grep -o "\"browser_download_url\":\"[^\"]*${asset_name}[^\"]*\"" | head -1 | cut -d'"' -f4)
        
        if [[ -n "$asset_url" ]]; then
            output_path="${TEMP_DIR}/${asset_name}"
            download_file "$asset_url" "$output_path" "$asset_name"
            
            if [[ -f "$output_path" ]]; then
                extract_archive "$output_path" "$DOWNLOAD_DIR"
                rm -f "$output_path"
            fi
        else
            write_info "Asset $asset_name not found in release (this is OK if not packaged)"
        fi
    done
    
    echo ""
    write_success "Setup complete!"
    echo ""
    write_info "Folder status:"
    [[ -d "${DOWNLOAD_DIR}/engine" ]] && echo "  ✓ engine/ extracted"
    [[ -d "${DOWNLOAD_DIR}/bin" ]] && echo "  ✓ bin/ extracted"
    echo ""
    write_info "Ready to run: python main.py"
}

# Run main function
main
