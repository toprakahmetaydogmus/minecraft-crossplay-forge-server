@echo off
chcp 65001 >nul
title Minecraft Crossplay 1-Click Server & Admin Suite
cd /d "%~dp0"

echo ===============================================================================
echo   ⚡ BAŞLATILIYOR: Minecraft Crossplay Sunucu + Admin Paneli + Auto Maker ⚡
echo ===============================================================================

echo [*] [1/2] Minecraft Forge 1.20.1 Sunucusu yeni pencerede başlatılıyor...
start "Minecraft Crossplay Forge 1.20.1 Server" cmd /k "start.bat"

echo [*] Sunucu başlatma sinyali verildi, 3 saniye bekleniyor...
timeout /t 3 /nobreak >nul

echo [*] [2/2] Ultimate Admin Paneli & Mimar Stüdyosu başlatılıyor...
start "Minecraft Admin Panel & Schematics Studio" python admin_panel.py

echo.
echo ===============================================================================
echo   [OK] Sunucu ve Admin Paneli aktif!
echo   [İPUCU] Auto Server Maker & AI Suite'i başlatmak için AUTO_BUILDER.bat
echo   çalıştırabilir veya Admin Paneli üstündeki mavi butona tıklayabilirsiniz.
echo ===============================================================================
timeout /t 3 >nul
exit
