@echo off
REM .githooks/post-clone.ps1
REM Automatically runs after git clone to restore binary files (Windows)
REM Install with: git config core.hooksPath .githooks

echo [LUCID] Post-Clone Hook: Restoring binary files...

if exist setup-binaries.ps1 (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File setup-binaries.ps1
    if %ERRORLEVEL% EQU 0 (
        echo [SUCCESS] Binary files restored automatically
    ) else (
        echo [WARNING] Binary restoration failed. Run .\setup-binaries.ps1 manually
    )
) else (
    echo [INFO] setup-binaries.ps1 not found - skipping automatic restoration
    echo [INFO] Run '.\setup-binaries.ps1' manually to restore binary files
)
