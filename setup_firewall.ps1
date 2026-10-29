# Güvenlik Duvarı Kuralları Ekleme Scripti
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Minecraft Crossplay Sunucusu Guvenlik Duvari Kural Ayari" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

try {
    # TCP 25565 - Java Portu
    $ruleJava = Get-NetFirewallRule -DisplayName "Minecraft Java Server (TCP 25565)" -ErrorAction SilentlyContinue
    if ($ruleJava) {
        Write-Host "[*] TCP 25565 kurali zaten mevcut, guncelleniyor..." -ForegroundColor Yellow
        Remove-NetFirewallRule -DisplayName "Minecraft Java Server (TCP 25565)"
    }
    New-NetFirewallRule -DisplayName "Minecraft Java Server (TCP 25565)" `
        -Direction Inbound `
        -LocalPort 25565 `
        -Protocol TCP `
        -Action Allow `
        -Profile Any `
        -Description "Minecraft Forge 1.20.1 Java giris portu" | Out-Null
    Write-Host "[OK] TCP 25565 (Java) Inbound kurali basariyla olusturuldu!" -ForegroundColor Green

    # UDP 19132 - Bedrock (Geyser) Portu
    $ruleBedrock = Get-NetFirewallRule -DisplayName "Minecraft Bedrock Geyser (UDP 19132)" -ErrorAction SilentlyContinue
    if ($ruleBedrock) {
        Write-Host "[*] UDP 19132 kurali zaten mevcut, guncelleniyor..." -ForegroundColor Yellow
        Remove-NetFirewallRule -DisplayName "Minecraft Bedrock Geyser (UDP 19132)"
    }
    New-NetFirewallRule -DisplayName "Minecraft Bedrock Geyser (UDP 19132)" `
        -Direction Inbound `
        -LocalPort 19132 `
        -Protocol UDP `
        -Action Allow `
        -Profile Any `
        -Description "Minecraft Bedrock GeyserMC giris portu" | Out-Null
    Write-Host "[OK] UDP 19132 (Bedrock Geyser) Inbound kurali basariyla olusturuldu!" -ForegroundColor Green

    Write-Host ""
    Write-Host "Tebrikler! Windows Guvenlik Duvari portlari basariyla acildi." -ForegroundColor Cyan
} catch {
    Write-Host "[HATA] Guvenlik duvari kurallari eklenemedi: $_" -ForegroundColor Red
    Write-Host "Lutfen bu scripti 'Yonetici Olarak Calistir' (Run as Administrator) secenegi ile baslatin." -ForegroundColor Yellow
}
