@echo off
title Windows Guvenlik Duvari Minecraft Port Ayarlayici
set "params=%*"
cd /d "%~dp0"

:: Yonetici haklari kontrolu ve kendini yukseltme (UAC Prompt)
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_script
) else (
    echo [*] Yonetici izinleri isteniyor...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~dpnx0\"\"' -Verb RunAs"
    exit /b
)

:run_script
echo [*] Guvenlik duvari kurallari ekleniyor...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_firewall.ps1"
echo.
pause
