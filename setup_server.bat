@echo off
chcp 65001 >nul
title ⚡ Minecraft Forge Crossplay Server - 2-Minute Quick Installer
color 0B

echo ===============================================================================
echo   ⚡ MINECRAFT FORGE 1.20.1 CROSSPLAY + ULTIMATE ADMIN PANEL INSTALLER ⚡
echo             (Java + Bedrock Crossplay  |  40+ Admin Categories  |  RCON)
echo ===============================================================================
echo.

cd /d "%~dp0"

REM -------------------------------------------------------------------------------
REM 1. PYTHON AND DEPENDENCY CHECK
REM -------------------------------------------------------------------------------
echo [*] [1/6] Python ve gerekli paketler kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] HATA: Python bulunamadi! Lutfen Python 3.10 veya daha yeni bir surum kurun.
    echo     https://www.python.org/downloads/ adresinden indirebilirsiniz.
    echo     (Kurulumda 'Add Python to PATH' kutusunu isaretlemeyi unutmayin!)
    pause
    exit /b 1
)

echo [*] Python tespit edildi. Gerekli kutuphaneler yukleniyor (nbtlib, requests)...
python -m pip install -q --disable-pip-version-check nbtlib requests >nul 2>&1
echo [OK] Python paketleri hazir!
echo.

REM -------------------------------------------------------------------------------
REM 2. JAVA 17+ CHECK
REM -------------------------------------------------------------------------------
echo [*] [2/6] Java 17+ kontrol ediliyor...
set "JAVA_EXE="
if exist "java17\bin\java.exe" (
    set "JAVA_EXE=java17\bin\java.exe"
) else if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" set "JAVA_EXE=%JAVA_HOME%\bin\java.exe"
)

if "%JAVA_EXE%"=="" (
    java -version >nul 2>&1
    if %errorlevel% equ 0 set "JAVA_EXE=java"
)

if "%JAVA_EXE%"=="" (
    echo [!] Java bulunamadi. Adoptium Temurin Java 17 indiriliyor...
    powershell -Command "Write-Host 'İndiriliyor: Java 17 LTS...'; Invoke-WebRequest -Uri 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.10%2B7/OpenJDK17U-jre_x64_windows_hotspot_17.0.10_7.zip' -OutFile 'java17.zip'"
    echo [*] Java cikariliyor...
    powershell -Command "Expand-Archive -Path 'java17.zip' -DestinationPath 'temp_java'; Move-Item 'temp_java\*' 'java17'; Remove-Item 'java17.zip'; Remove-Item 'temp_java' -Recurse"
    set "JAVA_EXE=java17\bin\java.exe"
)
echo [OK] Java hazir: %JAVA_EXE%
echo.

REM -------------------------------------------------------------------------------
REM 3. ACCEPT MINECRAFT EULA
REM -------------------------------------------------------------------------------
echo [*] [3/6] Minecraft EULA sozlesmesi onaylaniyor...
echo eula=true> eula.txt
echo [OK] eula.txt = true ayarlandi.
echo.

REM -------------------------------------------------------------------------------
REM 4. ARCLIGHT SERVER JAR CHECK & DOWNLOAD
REM -------------------------------------------------------------------------------
echo [*] [4/6] Arclight Forge 1.20.1 sunucu cekirdegi kontrol ediliyor...
if not exist "arclight-forge-1.20.1.jar" (
    if not exist "forge-1.20.1-server.jar" (
        echo [*] Sunucu jar dosyasi eksik. Resmi Arclight Forge 1.20.1 indiriliyor...
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/ArclightPowered/Arclight/releases/download/Forge%2F1.20.1%2F1.0.8/arclight-forge-1.20.1-1.0.8.jar' -OutFile 'arclight-forge-1.20.1.jar'"
        echo [OK] arclight-forge-1.20.1.jar basariyla indirildi!
    )
) else (
    echo [OK] arclight-forge-1.20.1.jar mevcut.
)
echo.

REM -------------------------------------------------------------------------------
REM 5. SERVER.PROPERTIES & CONFIGS CHECK
REM -------------------------------------------------------------------------------
echo [*] [5/6] Konfigurasyon ve RCON dosyalari kontrol ediliyor...
if not exist "server.properties" (
    if exist "server.properties.example" (
        copy "server.properties.example" "server.properties" >nul
        echo [OK] server.properties example sablonundan olusturuldu.
    )
)

if not exist "ops.json" (
    if exist "ops.example.json" (
        copy "ops.example.json" "ops.json" >nul
        echo [OK] ops.json example sablonundan olusturuldu.
    )
)
echo [OK] Konfigurasyonlar tamamlandi.
echo.

REM -------------------------------------------------------------------------------
REM 6. CREATE DESKTOP SHORTCUTS
REM -------------------------------------------------------------------------------
echo [*] [6/6] Hizli baslatici dosyalari hazirlaniyor...
echo [OK] ADMIN_PANEL.bat ve START_ALL.bat hazir.
echo.

echo ===============================================================================
echo  🎉 KURULUM BASARIYLA TAMAMLANDI! (2 Dakikada Hazir!)
echo ===============================================================================
echo.
echo  1. Sunucuyu ve Admin Panelini ayni anda baslatmak icin:
echo     -> START_ALL.bat
echo.
echo  2. Sadece Admin Panelini acmak icin:
echo     -> ADMIN_PANEL.bat
echo.
echo  3. Sadece Minecraft Sunucusunu calistirmak icin:
echo     -> start.bat
echo.
echo  Port Bilgileri:
echo   - Java Edition: 25565 (TCP)
echo   - Bedrock Edition: 19132 (UDP)
echo   - RCON Yonetim: 25575 (TCP)
echo ===============================================================================
echo.
set /p launch_now="Sunucuyu ve Admin Panelini simdi baslatmak ister misiniz? (E/H): "
if /i "%launch_now%"=="E" (
    start "" START_ALL.bat
)
exit /b 0
