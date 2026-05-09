@echo off
title Elyndria Chronicles Launcher
echo ================================================
echo   Elyndria Chronicles - Auto Updater + Launcher
echo ================================================
echo.

:: Change to the directory where this batch file is located
cd /d "%~dp0"

echo [1/3] Pulling latest updates from GitHub...
git pull origin main
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Git pull failed. Make sure you have Git installed and this is a valid repo folder.
    echo You can still try to run the game anyway.
    echo.
    pause
)

echo.
echo [2/3] Installing / updating Python requirements...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Could not install requirements. Make sure Python and pip are installed.
    echo Try running: pip install -r requirements.txt manually.
    echo.
    pause
)

echo.
echo [3/3] Launching Elyndria Chronicles...
echo.
python main.py

echo.
echo Game closed. Press any key to exit...
pause >nul
exit /b 0