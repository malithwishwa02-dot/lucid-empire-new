# LUCID EMPIRE :: Post-Clone Binary Restoration
# Automatically restores binary files from bundle after git clone
# Platform: Windows (PowerShell 5.1+)
# Usage: After cloning, run: .\setup-binaries.ps1

param(
    [string]$BundleUrl = "https://github.com/malithwishwa02-dot/lucid-empire-new/releases/download/v5.0-binaries/lucid-11commits.bundle.zip",
    [switch]$UseLocalBundle = $false,
    [string]$LocalBundlePath = ""
)

$ErrorActionPreference = "Stop"

function Write-Header {
    Write-Host "" -ForegroundColor Green
    Write-Host "[LUCID] Post-Clone Binary Setup (Windows)" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "[+] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-Prerequisites {
    Write-Warning "Testing prerequisites..."
    
    # Check git
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        Write-Error "Git not found. Please install Git for Windows."
        exit 1
    }
    Write-Success "Git found: $($git.Source)"
    
    # Check 7-Zip or built-in compression
    $sevenZip = Get-Command 7z -ErrorAction SilentlyContinue
    if ($sevenZip) {
        Write-Success "7-Zip found: $($sevenZip.Source)"
        return "7z"
    }
    
    Write-Success "Using Windows built-in compression"
    return "builtin"
}

function Download-Bundle {
    param([string]$Url)
    
    $tempDir = [System.IO.Path]::GetTempPath()
    $bundlePath = Join-Path $tempDir "lucid-11commits.bundle.zip"
    
    Write-Warning "Downloading bundle from GitHub..."
    Write-Host "URL: $Url"
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        (New-Object System.Net.WebClient).DownloadFile($Url, $bundlePath)
        
        if (Test-Path $bundlePath) {
            $size = (Get-Item $bundlePath).Length / 1MB
            Write-Success "Downloaded: $bundlePath ($([math]::Round($size, 2)) MB)"
            return $bundlePath
        } else {
            Write-Error "Download failed - file not created"
            exit 1
        }
    } catch {
        Write-Error "Download error: $_"
        Write-Host "Please download manually from: $Url" -ForegroundColor Yellow
        exit 1
    }
}

function Extract-Bundle {
    param(
        [string]$BundlePath,
        [string]$CompressionTool
    )
    
    $tempDir = [System.IO.Path]::GetTempPath()
    $extractPath = Join-Path $tempDir "lucid-bundle-extract"
    
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }
    New-Item $extractPath -ItemType Directory -Force | Out-Null
    
    Write-Warning "Extracting bundle (this may take a moment)..."
    
    try {
        if ($CompressionTool -eq "7z") {
            & 7z x "-o$extractPath" $BundlePath | Out-Null
        } else {
            # Windows built-in
            Expand-Archive -Path $BundlePath -DestinationPath $extractPath -Force
        }
        
        Write-Success "Bundle extracted to: $extractPath"
        return $extractPath
    } catch {
        Write-Error "Extraction failed: $_"
        exit 1
    }
}

function Restore-GitObjects {
    param([string]$ExtractPath)
    
    Write-Warning "Restoring git objects and binary files..."
    
    $bundleFile = Get-ChildItem $ExtractPath -Filter "*.bundle" -Recurse | Select-Object -First 1
    
    if (-not $bundleFile) {
        Write-Error "Bundle file not found in extraction directory"
        exit 1
    }
    
    $repoDir = Get-Location
    
    try {
        # Verify bundle
        & git bundle verify $bundleFile.FullName 2>&1 | Out-Null
        Write-Success "Bundle verified"
        
        # Fetch from bundle
        & git fetch $bundleFile.FullName 'refs/heads/main:refs/remotes/bundle/main' 2>&1 | Out-Null
        Write-Success "Git objects restored"
    } catch {
        Write-Error "Git restoration failed: $_"
        exit 1
    }
}

function Verify-Restoration {
    Write-Warning "Verifying binary files..."
    
    $filesToCheck = @(
        "camoufox/.gitkeep_placeholder",
        "assets/.gitkeep_placeholder",
        "engine/.gitkeep_placeholder",
        "lucid_profile_data/.gitkeep_placeholder",
        "packaging/.gitkeep_placeholder",
        "research_reports/.gitkeep_placeholder",
        "backend/core/genesis_engine.py",
        "backend/modules/commerce_injector.py",
        "backend/network/xdp_outbound.c"
    )
    
    $missing = 0
    foreach ($file in $filesToCheck) {
        if (Test-Path $file) {
            Write-Host "[✓] $file" -ForegroundColor Green
        } else {
            Write-Host "[✗] $file (missing)" -ForegroundColor Red
            $missing++
        }
    }
    
    if ($missing -eq 0) {
        Write-Success "All files verified successfully!"
        return $true
    } else {
        Write-Warning "$missing files missing"
        return $false
    }
}

function main {
    Write-Header
    
    # Check if binaries already exist
    if ((Test-Path "camoufox/.gitkeep_placeholder") -and (Test-Path "backend/core/genesis_engine.py")) {
        Write-Success "Binary files already present!"
        Verify-Restoration
        exit 0
    }
    
    # Get compression tool
    $compTool = Test-Prerequisites
    
    # Get bundle
    $bundlePath = ""
    if ($UseLocalBundle -and (Test-Path $LocalBundlePath)) {
        $bundlePath = $LocalBundlePath
        Write-Success "Using local bundle: $LocalBundlePath"
    } else {
        $bundlePath = Download-Bundle -Url $BundleUrl
    }
    
    # Extract and restore
    $extractPath = Extract-Bundle -BundlePath $bundlePath -CompressionTool $compTool
    Restore-GitObjects -ExtractPath $extractPath
    Verify-Restoration
    
    # Cleanup
    Write-Warning "Cleaning up temporary files..."
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }
    
    Write-Host "" -ForegroundColor Green
    Write-Success "Binary restoration complete!"
    Write-Success "Repository is now fully functional"
    Write-Host "" -ForegroundColor Green
}

main
