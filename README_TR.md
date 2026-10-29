<div align="center">

# ⚔️ Minecraft Crossplay Forge 1.20.1 & Gelişmiş Admin Paneli
### **40+ Admin Sekmesi, 160+ Tek Tıkla Yapı İnşası ve Java-Bedrock Çapraz Platform Desteği**

[![GitHub Stars](https://img.shields.io/github/stars/toprakahmetaydogmus/minecraft-crossplay-forge-server?style=for-the-badge&logo=github&color=gold)](https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server/stargazers)
[![Minecraft Version](https://img.shields.io/badge/Minecraft-1.20.1-brightgreen?style=for-the-badge&logo=minecraft)](https://www.minecraft.net/)
[![Forge Version](https://img.shields.io/badge/Forge-47.2.20-orange?style=for-the-badge)](https://files.minecraftforge.net/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/Lisans-MIT-purple?style=for-the-badge)](LICENSE)
[![Crossplay](https://img.shields.io/badge/Çapraz%20Platform-Java%20%2B%20Bedrock-cyan?style=for-the-badge)](https://geysermc.org/)

<br/>

> **⭐ Bu projeyi beğendiyseniz, lütfen GitHub üzerinden yıldız vermeyi unutmayın!**  
> [![Star on GitHub](https://img.shields.io/badge/⭐%20Depoya%20Yıldız%20Ver-Gold?style=for-the-badge)](https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server)

[🇬🇧 Click Here for English Documentation (README.md)](README.md)

</div>

---

## 🌟 Neden Bu Sunucu Paketini Seçmelisiniz?

Modlu, eklentili ve telefon/konsol destekli bir Minecraft sunucusu kurmak normalde saatler süren karmaşık ayarlamalar gerektirir.

**Bu proje ile en acemi kullanıcı bile 2 dakika içinde eksiksiz bir sunucuya ve gelişmiş bir yönetim paneline sahip olabilir!**

---

## ✨ Öne Çıkan Özellikler

### 🏛️ 1. Schematics Mimar Stüdyosu (rom1504 Veri Seti Tabanlı)
- **160+ Hazır Yapı**: Modern lüks villalar, ortaçağ taş kaleleri, kütük dağ evleri, gökdelenler, yeraltı nükleer sığınakları, kızıltaş hasat çiftlikleri, piramitler ve antik tapınaklar.
- **rom1504/minecraft-schematics-dataset Mimarisi**: Veri setindeki popüler kategori yapısına uygun hazır şablonlar.
- **İleri Seviye Yerleştirme Ayarları**:
  - 🔄 **Döndürme (Rotation)**: 0°, 90°, 180°, 270°.
  - 🪞 **Aynalama (Mirroring)**: Yok, Sağ-Sol, Ön-Arka.
  - 🎯 **Hedefleme**: Oyuncuya Göre (`~ ~ ~`) veya Doğrudan Dünya X/Y/Z Koordinatlarına.
  - 🧹 **Otomatik Zemin & Hava Temizleyici**: İnşaata başlamadan önce ağaçları ve zemin pürüzlerini sıfırlar.
  - ↩️ **Geri Alma (Undo) Motoru**: Yanlış yere konulan bir yapıyı tek tıkla eski haline getirir.
  - 📂 **Harici `.schem` ve `.nbt` Yükleyici**: İstediğiniz dosyayı panelden seçip haritaya aktarabilirsiniz.

### 🎮 2. Java & Bedrock Çapraz Platform (Crossplay)
- **GeyserMC & Floodgate Entegrasyonu**: Bilgisayar (Java), Telefon, Tablet (iOS / Android) ve Konsol (Xbox, PS, Switch) oyuncuları aynı anda oynayabilir.
- **Portlar**:
  - **Java Giriş**: `25565` (TCP)
  - **Bedrock (Mobil/Konsol)**: `19132` (UDP)
  - **RCON Yönetim**: `25575` (TCP)

### 🎛️ 3. 40+ Kategorili Cyberpunk Admin Paneli
- **Yüksek Hızlı RCON**: Komutlar gecikmesiz iletilir, bağlantı kopsa dahi otomatik bağlanır.
- **Canlı Sunucu Konsolu**: Renkli log takibi ve doğrudan komut gönderme satırı.
- **Tek Tıkla Fonksiyonlar**:
  - 💰 **Akçe ve Ekonomi Sistemi**: Scoreboard tabanlı canlı bakiye, periyodik otomatik maaş dağıtıcısı.
  - 🏪 **Özel NPC Tüccarlar**: Silahçı, Mimar, Simyacı, Çiftçi, Kızıltaşçı ve Karaborsacı NPC dükkanları.
  - ⚡ **32k Tanrı Eşyaları**: Level 255 büyü seviyesine sahip tek atan kılıçlar, tanrı kazmaları.
  - 🎪 **Sunucu Etkinlikleri & Boss**: Meteor yağmuru, altın yağmuru, zombi istilası, boss arenaları.
  - 🤡 **Troll & Oyuncu Yönetimi**: Zindana atma, dondurma, roketleme, kafasına örs atma, envanter temizleme.
  - 🧹 **Anti-Lag & FPS Koruyucu**: Tek tıkla yerdeki çöpleri silme, TPS artırma, gamerule kalkanı.

### 🛡️ 4. Sıfır Sızıntı & Gizlilik Mimarisi
- **IP Sızıntısı Yok**: Özel ağ IP'leri ve tüneller açıkta bırakılmaz.
- **Dinamik RCON Ayarı**: Şifreler `server.properties` veya `.env` üzerinden otomatik okunur.
- **Güvenli `.gitignore`**: Oyuncu verileri, kayıtlı dünyalar ve log dosyaları asla GitHub'a sızmaz.

---

## ⚡ 2 Dakikada Hızlı Kurulum

### 🪟 Windows İçin
```bat
# 1. Depoyu klonlayın
git clone https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server.git
cd minecraft-crossplay-forge-server

# 2. Kurulum sihirbazını çalıştırın
setup_server.bat
```
*Sihirbaz Java 17 ve Python kütüphanelerini (`nbtlib`, `requests`) otomatik kontrol eder, çekirdek dosyalarını indirir ve sunucuyu hazır hale getirir!*

Sunucuyu ve Admin Panelini aynı anda açmak için:
```bat
START_ALL.bat
```

---

### 🐧 Linux / macOS İçin
```bash
# 1. Depoyu klonlayın
git clone https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server.git
cd minecraft-crossplay-forge-server

# 2. Kurulumu çalıştırın
chmod +x setup_server.sh
./setup_server.sh

# 3. Başlatın
./run.sh
python3 admin_panel.py
```

---

## 🛠️ Dahili Modlar ve Eklentiler

| Bileşen | Tür | Açıklama |
|---|---|---|
| **Arclight Forge 1.20.1** | Çekirdek | Forge modları ile Spigot eklentilerini aynı anda çalıştırır |
| **Geyser-Spigot & Floodgate** | Eklenti | Bedrock oyuncularının Java sunucusuna bağlanmasını sağlar |
| **Just Enough Items (JEI)** | Mod | Oyun içi tarif ve eşya listesi görüntüleyici |
| **Mouse Tweaks** | Mod | Envanterde ve sandıklarda hızlı eşya düzenleme modu |
| **FerriteCore** | Mod | Sunucunun RAM tüketimini büyük oranda düşürür |
| **TAB** | Eklenti | Animasyonlu TAB listesi, skor tablosu ve unvanlar |
| **EssentialsX** | Eklenti | Işınlanmalar, ev kaydetme, kitler ve spawn yönetimi |
| **EconomyShopGUI & Vault** | Eklenti | Akçe ekonomisi ve GUI market sistemi |
| **GrimAC** | Eklenti | Hile önleyici gelişmiş paket filtresi |

---

## 🎮 Hızlı Admin Komut Rehberi

| İşlem | Oyun İçi Komut |
|---|---|
| **Yaratıcı Moduna Geç** | `/gamemode creative` |
| **Dünyayı Diske Kaydet** | `/save-all flush` |
| **Yerdeki Çöpleri Temizle** | `/kill @e[type=item]` |
| **Oyuncuya 50.000 Akçe Ver** | `/scoreboard players add <oyuncu> akce 50000` |
| **Market Arayüzünü Aç** | `/shop` veya `/n` |
| **Altın Kürekle Arsa Kapat** | `/arsa` veya `/claim` |
| **Güvenli Takas Başlat** | `/takas <oyuncu>` veya `/trade <oyuncu>` |

---

## 🤝 Katkıda Bulunma & Yıldız Verme

Projeyi geliştirmemize yardımcı olmak isterseniz:
1. Depoyu Fork'layın
2. Yeni Dal Açın (`git checkout -b ozellik/YeniOzellik`)
3. Değişiklikleri Kaydedin (`git commit -m 'Yeni ozellik eklendi'`)
4. Gönderin (`git push origin ozellik/YeniOzellik`)
5. Pull Request (PR) Açın

Projeyi beğendiyseniz sağ üstten **⭐ Yıldız (Star)** vermeyi unutmayın!

---

## 📄 Lisans
Bu proje **MIT Lisansı** altında sunulmaktadır.
