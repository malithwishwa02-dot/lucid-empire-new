@echo off
REM Cleanup Large Files from Repository
REM Removes fonts, binaries, and large assets to reduce repo size

cls
color 0B
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║          LUCID EMPIRE - Repository Size Optimization                  ║
echo ║     Removing Large Files (fonts, binaries, externals)                  ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion
set REMOVED_COUNT=0
set TOTAL_SIZE=0

REM Remove large binaries
echo [*] Removing large binary files...
for %%F in (engine\node.exe engine\python315.dll engine\libcrypto-3.dll engine\tcl86t.dll engine\tk86t.dll engine\sqlite3.dll engine\api.json engine\registry.json engine\background.gif engine\disk.icns lucid-11commits.bundle lucid-11commits.bundle.zip) do (
    if exist "%%F" (
        echo   [REMOVE] %%F
        del /Q "%%F" >nul 2>&1
        git rm --cached "%%F" >nul 2>&1
        set /A REMOVED_COUNT+=1
    )
)

REM Remove font directory
if exist "engine\bundle\fonts" (
    echo [*] Removing font directory...
    echo   [REMOVE] engine\bundle\fonts\
    rmdir /S /Q "engine\bundle\fonts" >nul 2>&1
    git rm -r --cached "engine\bundle\fonts" >nul 2>&1
)

REM Remove TTF/TTC files
echo [*] Removing font files...
for /R engine %%F in (*.ttf *.ttc) do (
    if exist "%%F" (
        echo   [REMOVE] %%~nxF
        del /Q "%%F" >nul 2>&1
        git rm --cached "%%F" >nul 2>&1
        set /A REMOVED_COUNT+=1
    )
)

REM Remove DLL files
echo [*] Removing DLL files...
for /R engine %%F in (*.dll) do (
    if exist "%%F" (
        echo   [REMOVE] %%~nxF
        del /Q "%%F" >nul 2>&1
        git rm --cached "%%F" >nul 2>&1
        set /A REMOVED_COUNT+=1
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                        CLEANUP COMPLETE                               ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo Summary:
echo   Files Removed: !REMOVED_COUNT!
echo.
echo Next Steps:
echo   1. git add .gitignore
echo   2. git commit -m "CLEANUP: Remove large binaries and fonts"
echo   3. git push origin main --force
echo.
pause
