@echo off
chcp 65001 >nul
title Minecraft Crossplay 1-Click Server & Admin Launcher
cd /d "%~dp0"

echo ===============================================================================
echo   ⚡ BASLATILIYOR: Minecraft Crossplay Forge Sunucusu + Admin Paneli ⚡
echo ===============================================================================

echo [*] [1/2] Minecraft Sunucusu yeni pencerede baslatiliyor...
start "Minecraft Crossplay Forge 1.20.1 Server" cmd /k "start.bat"

echo [*] Sunucu baslatma sinyali verildi, 3 saniye bekleniyor...
timeout /t 3 /nobreak >nul

echo [*] [2/2] Ultimate Admin Paneli & Mimar Studyosu baslatiliyor...
start "Minecraft Admin Panel & Schematics Studio" python admin_panel.py

echo.
echo [OK] Tum sistemler baslatildi! Bu pencereyi kapatabilirsiniz.
timeout /t 2 >nul
exit
