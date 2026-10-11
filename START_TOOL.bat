@echo off
title TDL Media Downloader Pro - Windows Edition
color 0b
cls
echo ======================================================================
echo          TDL MEDIA DOWNLOADER PRO - WINDOWS EDITION
echo          Multi-threaded Video ^& Poster High-Speed Downloader
echo ======================================================================
echo.
echo [1/2] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ and add to PATH.
    pause
    exit /b
)

echo [2/2] Launching TDL Media Downloader Server and Browser...
python run_tool.py
pause
