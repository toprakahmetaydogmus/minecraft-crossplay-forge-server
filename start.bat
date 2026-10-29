@echo off
chcp 65001 >nul
title Crossplay Forge 1.20.1 Server (Java + Bedrock)

echo =====================================================================
echo       CROSSPLAY MINECRAFT FORGE 1.20.1 SUNUCU BASLATICISI
echo                   (Java + Bedrock Geyser Crossplay)
echo =====================================================================
echo.

set SERVER_DIR=%~dp0
cd /d "%SERVER_DIR%"

REM 1. Java Ortami Tespiti (Java 21 / Java 17)
set "JAVA_BIN="
if exist "C:\Program Files\Eclipse Adoptium\java-runtime-delta\bin\java.exe" (
    set "JAVA_BIN=C:\Program Files\Eclipse Adoptium\java-runtime-delta\bin\java.exe"
    echo [*] Sistemdeki Optimize Java 21 LTS tespit edildi.
) else if exist "%SERVER_DIR%java17\bin\java.exe" (
    set "JAVA_BIN=%SERVER_DIR%java17\bin\java.exe"
    echo [*] Dahili Adoptium Temurin Java 17 kullaniliyor.
) else if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" (
        set "JAVA_BIN=%JAVA_HOME%\bin\java.exe"
        echo [*] JAVA_HOME uzerinden Java kullaniliyor.
    )
)

if "%JAVA_BIN%"=="" (
    set "JAVA_BIN=java"
    echo [*] Sistem PATH uzerindeki varsayilan Java kullaniliyor.
)

echo [*] Calistirilacak Java Surumu:
"%JAVA_BIN%" -Xshare:off -version
echo.

REM 2. Sunucu Jar Dosyasini Belirle
set "SERVER_JAR=arclight-forge-1.20.1.jar"
if not exist "%SERVER_JAR%" set "SERVER_JAR=forge-1.20.1-server.jar"
if not exist "%SERVER_JAR%" (
    echo [HATA] Sunucu jar dosyasi bulunamadi.
    pause
    exit /b 1
)

REM Port 25565 zaten acik mi kontrol et
netstat -ano | findstr ":25565.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo [BILGI] Minecraft sunucusu ZATEN SU ANDA AKTIF VE CALISIYOR!
    echo         Port 25565 su anda arkadaslarinizin girisi icin acik.
    echo =====================================================================
    echo.
    echo Arkadaslariniz ve siz su anda oyuna baglanabilirsiniz.
    echo Sunucuyu kapatmak icin masaustundeki SUNUCUYU_KAPAT.bat dosyasini kullanin.
    echo.
    pause
    exit /b 0
)

REM Eski kilit dosyasini temizle (Eger sunucu aniden kapandiysa)
if exist "world\session.lock" del /f /q "world\session.lock" >nul 2>&1

echo [*] Sunucu Jar: %SERVER_JAR%
echo [*] Bellek: Min 1.5GB - Max 3GB (Ultra Hafif 3GB Aikar G1GC Optimize)
echo [*] Java Baglanti Portu: 25565 (TCP)
echo [*] Bedrock Baglanti Portu: 19132 (UDP)
echo.
echo Sunucu baslatiliyor... Kapatmak icin konsola 'stop' yaziniz.
echo =====================================================================
echo.

REM 3. Optimize Aikar G1GC ve Modern Java Erisim Bayraklari (3GB RAM Optimize)
"%JAVA_BIN%" -Xms1536M -Xmx3072M -Xshare:off ^
  --add-opens=java.base/java.lang=ALL-UNNAMED ^
  --add-opens=java.base/java.lang.invoke=ALL-UNNAMED ^
  --add-opens=java.base/java.lang.reflect=ALL-UNNAMED ^
  --add-opens=java.base/java.util=ALL-UNNAMED ^
  -XX:+UseG1GC ^
  -XX:+ParallelRefProcEnabled ^
  -XX:MaxGCPauseMillis=200 ^
  -XX:+UnlockExperimentalVMOptions ^
  -XX:+DisableExplicitGC ^
  -XX:+AlwaysPreTouch ^
  -XX:G1NewSizePercent=20 ^
  -XX:G1MaxNewSizePercent=30 ^
  -XX:G1ReservePercent=15 ^
  -XX:G1HeapWastePercent=5 ^
  -XX:G1MixedGCCountTarget=4 ^
  -XX:InitiatingHeapOccupancyPercent=20 ^
  -XX:G1MixedGCLiveThresholdPercent=90 ^
  -XX:G1RSetUpdatingPauseTimePercent=5 ^
  -XX:SurvivorRatio=32 ^
  -XX:+PerfDisableSharedMem ^
  -XX:MaxTenuringThreshold=1 ^
  -Dfile.encoding=UTF-8 ^
  -Duser.timezone=Europe/Istanbul ^
  -Djava.net.preferIPv4Stack=true ^
  -jar "%SERVER_JAR%" nogui

echo.
echo =====================================================================
echo Sunucu kapandi.
echo =====================================================================
pause
