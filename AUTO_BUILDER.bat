@echo off
chcp 65001 >nul
title Auto Minecraft Server Maker & AI Engineer Pro
cd /d "%~dp0"
start "" python auto_server_maker.py
exit
