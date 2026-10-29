@echo off
chcp 65001 >nul
title Minecraft Admin Panel & Builder Studio
cd /d "%~dp0"
start "" python admin_panel.py
exit
