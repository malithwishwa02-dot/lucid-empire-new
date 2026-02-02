# setup_externals.ps1
# Downloads and extracts external dependencies (engine/, bin/) after cloning Lucid Empire
# Usage: .\setup_externals.ps1
# Note: Requires curl or wget, and tar utility

param(
    [string]$ReleaseVersion = "latest",
    [switch]$Force = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Lucid Empire - External Dependencies Setup                        ║" -ForegroundColor Cyan
Write_Host "║  Downloading: engine/ and bin/ folders                             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$REPO_OWNER = "malithwishwa02-dot"
$REPO_NAME = "lucid-empire-new"
$GITHUB_API = "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME"
$DOWNLOAD_DIR = $PSScriptRoot
$TEMP_DIR = Join-Path $DOWNLOAD_DIR ".externals_temp"

# Color helpers
function Write-Success { param([string]$msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Error-Custom { param([string]$msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Info { param([string]$msg) Write-Host "ℹ $msg" -ForegroundColor Cyan }

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    $curl_exists = (Get-Command curl -ErrorAction SilentlyContinue) -ne $null
    $wget_exists = (Get-Command wget -ErrorAction SilentlyContinue) -ne $null
    $tar_exists = (Get-Command tar -ErrorAction SilentlyContinue) -ne $null
    
    if (-not ($curl_exists -or $wget_exists)) {
        Write-Error-Custom "Neither curl nor wget found. Please install curl or wget."
        Write-Host ""
        Write-Host "Manual installation:"
        Write-Host "1. Download engine.tar.gz from: https://github.com/$REPO_OWNER/$REPO_NAME/releases/$ReleaseVersion"
        Write-Host "2. Download bin.tar.gz from: https://github.com/$REPO_OWNER/$REPO_NAME/releases/$ReleaseVersion"
        Write-Host "3. Extract both to repository root:"
        Write-Host "   tar -xzf engine.tar.gz"
        Write-Host "   tar -xzf bin.tar.gz"
        exit 1
    }
    
    if (-not $tar_exists) {
        Write-Error-Custom "tar utility not found. Please install tar (comes with Git Bash or WSL)."
        exit 1
    }
    
    Write-Success "Prerequisites verified (curl/wget and tar available)"
}

# Get release info
function Get-ReleaseInfo {
    Write-Info "Fetching release information..."
    
    try {
        if ($ReleaseVersion -eq "latest") {
            $release = Invoke-RestMethod "$GITHUB_API/releases/latest" -ErrorAction Stop
        } else {
            $release = Invoke-RestMethod "$GITHUB_API/releases/tags/$ReleaseVersion" -ErrorAction Stop
        }
        
        return $release
    } catch {
        Write-Error-Custom "Failed to fetch release info from GitHub: $_"
        exit 1
    }
}

# Download file
function Download-File {
    param([string]$URL, [string]$OutputPath, [string]$FileName)
    
    Write-Info "Downloading $FileName..."
    
    try {
        if (Get-Command curl -ErrorAction SilentlyContinue) {
            curl.exe -L -o "$OutputPath" "$URL" -progress
        } else {
            wget.exe -O "$OutputPath" "$URL"
        }
        
        if (Test-Path $OutputPath) {
            Write-Success "Downloaded: $FileName"
            return $true
        }
    } catch {
        Write-Error-Custom "Failed to download $FileName : $_"
        return $false
    }
}

# Extract archive
function Extract-Archive {
    param([string]$ArchivePath, [string]$DestinationPath)
    
    $FileName = Split-Path -Leaf $ArchivePath
    Write-Info "Extracting $FileName to $DestinationPath..."
    
    try {
        tar -xzf "$ArchivePath" -C "$DestinationPath"
        Write-Success "Extracted: $FileName"
        return $true
    } catch {
        Write-Error-Custom "Failed to extract $FileName : $_"
        return $false
    }
}

# Main
try {
    Test-Prerequisites
    
    # Check if already extracted
    $engine_exists = Test-Path (Join-Path $DOWNLOAD_DIR "engine") -PathType Container
    $bin_exists = Test-Path (Join-Path $DOWNLOAD_DIR "bin") -PathType Container
    
    if (($engine_exists -or $bin_exists) -and -not $Force) {
        Write-Host ""
        Write-Info "External folders already present:"
        if ($engine_exists) { Write-Host "  ✓ engine/" }
        if ($bin_exists) { Write-Host "  ✓ bin/" }
        Write-Host ""
        Write-Info "Use -Force to re-download and overwrite"
        exit 0
    }
    
    # Create temp directory
    if (-not (Test-Path $TEMP_DIR)) {
        New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null
    }
    
    # Get release info
    $release = Get-ReleaseInfo
    Write-Success "Found release: $($release.tag_name)"
    Write-Host ""
    
    # Download files
    $downloads = @(
        @{ name = "engine.tar.gz"; asset = "engine.tar.gz" },
        @{ name = "bin.tar.gz"; asset = "bin.tar.gz" }
    )
    
    foreach ($download in $downloads) {
        $asset = $release.assets | Where-Object { $_.name -eq $download.asset }
        
        if ($asset) {
            $outputPath = Join-Path $TEMP_DIR $download.name
            Download-File -URL $asset.browser_download_url -OutputPath $outputPath -FileName $download.name
            
            if (Test-Path $outputPath) {
                Extract-Archive -ArchivePath $outputPath -DestinationPath $DOWNLOAD_DIR
                Remove-Item $outputPath -Force
            }
        } else {
            Write-Info "Asset $($download.name) not found in release (this is OK if not packaged)"
        }
    }
    
    Write-Host ""
    Write-Success "Setup complete!"
    Write-Host ""
    Write-Info "Folder status:"
    if (Test-Path (Join-Path $DOWNLOAD_DIR "engine")) { Write-Host "  ✓ engine/ extracted" }
    if (Test-Path (Join-Path $DOWNLOAD_DIR "bin")) { Write-Host "  ✓ bin/ extracted" }
    Write-Host ""
    Write-Info "Ready to run: python main.py"
    
} catch {
    Write-Error-Custom "Setup failed: $_"
    if (Test-Path $TEMP_DIR) {
        Remove-Item $TEMP_DIR -Recurse -Force
    }
    exit 1
} finally {
    if (Test-Path $TEMP_DIR) {
        Remove-Item $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue
    }
}
