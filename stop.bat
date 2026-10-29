@echo off
chcp 65001 >nul
title Minecraft Sunucusunu Kapat

echo =====================================================================
echo                MINECRAFT SUNUCUSUNU GUVELE KAPATMA
echo =====================================================================
echo.

set SERVER_DIR=%~dp0
cd /d "%SERVER_DIR%"

echo [*] Sunucuya guvenli dunya kaydi ve kapatma komutu iletiliyor...
python graceful_stop.py

echo.
echo =====================================================================
echo [OK] Islem tamamlandi.
echo =====================================================================
ping 127.0.0.1 -n 3 >nul
