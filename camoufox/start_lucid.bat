@echo off
REM LUCID EMPIRE :: WINDOWS LAUNCH PROTOCOL v5.0
SETLOCAL ENABLEEXTENSIONS
SET PROFILE_ID=%1

echo ===============================================
echo    LUCID EMPIRE :: WINDOWS LAUNCH SEQUENCE
echo    TARGET PROFILE: %PROFILE_ID%
echo ===============================================

IF "%PROFILE_ID%"=="" (
    echo [!] ERROR: No Profile ID received from Commander.
    echo     USAGE: start_lucid.bat ^<UUID^>
    exit /b 1
)

REM --- UAC Elevation Check ---
NET SESSION >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [!] PERMISSION: User is not Admin.
    echo [*] ESCALATION: Requesting UAC elevation via PowerShell...
    powershell -Command "Start-Process '%~f0' -ArgumentList '%PROFILE_ID%' -Verb RunAs"
    exit /b
)

echo [*] ELEVATION: GRANTED (ADMIN).

IF EXIST "venv\Scripts\activate" (
    CALL venv\Scripts\activate
)

IF EXIST "lucid_launcher.py" (
    echo [*] CORE: Handoff to Lucid Engine...
    python lucid_launcher.py --launch "%PROFILE_ID%" --mode manual
) ELSE (
    echo [!] CRITICAL: lucid_launcher.py not found in current directory.
    echo     PATH: %cd%
    exit /b 1
)

IF %ERRORLEVEL% NEQ 0 (
    echo [!] Launcher returned error %ERRORLEVEL%.
    PAUSE
)

echo [*] SESSION TERMINATED.
ENDLOCAL
