# Tasarım Belgesi: Minecraft Sunucu Admin Paneli, Casino & Kumarhane, Mega Yapı Kataloğu ve Anti-Xray Kalkanı

**Tarih:** 2026-10-28  
**Durum:** İncelendi & Onaylandı  
**Hedef:** Admin panelindeki UI taşma/küçültme sorunlarını sıfıra indirmek, interaktif Casino/Kumarhane sistemlerini eksiksiz kurmak, 25+ yeni devasa yapıyı oto-inşaat sistemine dahil etmek ve X-Ray doku paketlerini (resource pack) Engine Mode 2 Obfuscation ile tamamen kör etmek.

---

## 1. Problem Tanımı ve Kullanıcı İhtiyaçları
1. **Pencere Küçüldüğünde Menülerin Kaybolması (UI Clipping)**:
   - Mevcut `admin_panel.py` uygulamasında 24 sekme yatay `ttk.Notebook` çubuğunda yan yana dizilmektedir.
   - Ekran çözünürlüğü daraldığında veya pencere boyutu küçültüldüğünde sekmeler ekranın sağına taşarak tamamen görünmez hale gelmektedir.
   - Üst kontrol şeridi (ribbon) ve blok merkezi de sabit genişlikli yatay `pack` kullanmaktadır.
2. **Casino ve Kumarhane Eksiklikleri**:
   - Oyuncuların oyun içinde kol çekerek veya basarak oynayabileceği hazır mekanik slot makineleri, rulet ve blackjack masaları, şans kasaları ve lüks Las Vegas kumarhane sarayı eksiktir.
   - Panelden doğrudan tetiklenebilen, animasyonlu (Title, Subtitle, Note Block sesleri ve Scoreboard Akçe ödüllü) interaktif kumar motoru gereklidir.
3. **Yapı Sayısının Yetersizliği**:
   - Mevcut oto-inşaat kataloğunda yalnızca 17 yapı bulunmaktadır. Kullanıcı çok daha fazla, hazır ve devasa yapılar istemektedir.
4. **Anti-Xray Çalışmama Sorunu & Kaynak Paketleri**:
   - `config/antixray.toml` dosyasında mod `enabled = false` durumundadır ve Engine Mode 3 eksik yapılandırılmıştır.
   - Saydam doku paketi (X-Ray texture pack) kullanan oyuncular taş blokları şeffaf görerek cevherleri doğrudan bulabilmektedir.

---

## 2. Mimari Çözümler & Yaklaşımlar

### Seçilen Yaklaşım: Modern Responsive Sidebar + Canlı Hibrit Casino & Engine Mode 2 Obfuscation
- **UI Mimarisi**:
  - Yatay sekmeler yerine sol tarafta şık, simgeli, dikey kaydırılabilir ve anlık filtrelenebilir bir **Kategori Sidebar'ı** (`tk.Canvas` + `Scrollbar`).
  - Üst tarafta hızlı erişim için **Kategori Dropdown (Combobox)** ve arama kutusu.
  - Sağ tarafta seçili kategoriye ait buton kartlarını barındıran **Responsive Grid**. Pencere genişliği algılanarak (`<Configure>` olayı) sütun sayısı dinamik olarak (1, 2 veya 3 sütun) ayarlanır; hiçbir kart veya buton ekrandan taşmaz.
  - Fare tekerleği (MouseWheel) doğrudan imlecin üzerinde bulunduğu canvas'a bağlanarak pürüzsüz kaydırma sağlanır.
  - Üst şerit (Ribbon) ve Blok Merkezi, dar ekranlarda da düzenli görünecek şekilde çift satırlı veya esnek yerleşime kavuşturulur.

- **Casino & Kumarhane Sistemi**:
  - **İn-Game Fiziksel Makineler & Masalar**:
    - Kollu 3 Çarklı Fonksiyonel Slot Makinesi (Polished Blackstone, Altın, Dropper/Dispenser, Şalter/Kol, Nota Bloğu, Kazanç Hunisi).
    - Lüks Rulet Masası (Kırmızı/Siyah yünler, dönen mekanizma, bahis alanları).
    - 21 (Blackjack) Masası (Yeşil çuha, dağıtıcı koltuğu, oyuncu bölmeleri).
    - Yazı-Tura & Zar Düellosu Standı.
    - Jackpot ve Gizemli Şans Kasaları (Kazanç & Troll riskli).
    - Devasa Las Vegas Casino Palas Kompleksi (Işıklı neon giriş, çift katlı salon, VIP oda).
    - Yeraltı Gizli Kumarhanesi (Gizli kitaplık girişi, loş fenerler).
  - **Panelden Canlı Kumar & Loto Motoru**:
    - Animasyonlu Slot Çevirme (3 aşamalı çark animasyonu, Title/Subtitle, sesler, jackpot ödülü).
    - Rulet Çevirme (Kırmızı/Siyah/Yeşil, 1-36 sayı çekilişi ve bakiye aktarımı).
    - Zar Atma & Yazı-Tura (Canlı sonuçlar ve sesler).
    - Sunucu Geneli Loto/Piyango Çekilişi (Tüm online oyuncular arasından kazananı seçme ve akçe ödülü).

- **Mega Yapı Kataloğu (25+ Yeni Yapı)**:
  - 🏙️ 30 Blokluk Modern Cam & Çelik Siber Gökdelen
  - 🏰 Dev Gotik Katedral & Saat Kulesi
  - ⛩️ Büyük Japon Torii Tapınağı & Zen Bahçesi
  - 🌊 Atlantis Su Altı Cam Kubbe Şehri
  - 🏦 Merkez Bankası & Aşılmaz Kasa Dairesi
  - 🏟️ Dev Futbol & Olimpiyat Stadyumu
  - 🎡 Lunapark & Işıklı Dönme Dolap
  - 🛫 Modern Havalimanı & Işıklı Uçak Pisti
  - ⚓ Dev 3 Direkli Korsan Kalyonu
  - 🏯 Büyük Ortaçağ Hanı & Taverna
  - 🏎️ Formula 1 Yarış Pisti & Pit Stop
  - 🚀 Uzay Üssü & Roket Fırlatma Rampası
  - 🌲 Dev Elf Ağaç Evi (Y: 25)
  - 🌴 Tropik Ada Tatil Köyü & Su Bungalovları
  - 🌾 Endüstriyel Dev Çiftlik & Tahıl Silosu Kompleksi
  - 🕌 Tarihi Kervansaray & Şadırvan
  - 🧪 Büyük Simya & Büyücülük Akademisi
  - ❄️ Kutup Araştırma İstasyonu & İglo Köyü
  - 🛸 UFO & Uzaylı İniş Alanı
  - 🛡️ Askeri Kışla & Helikopter Pisti
  - 🌋 Netherite Lav Sarayı & Cehennem Kalesi
  - Ve daha fazlası (Toplamda 42+ yapı seçeneği).

- **Anti-Xray & Kaynak Paketi Körleştirme (Engine Mode 2)**:
  - `config/antixray.toml`:
    - `enabled = true`
    - `[overworld]`: `engineMode = 2`, `maxBlockHeight = 320`, `hiddenBlocks` ve `replacementBlocks` tam liste (Tüm elmas, zümrüt, altın, demir, antik kalıntı, sandıklar).
    - `[the_nether]`: `enabled = true`, `engineMode = 2`, `maxBlockHeight = 128`, `lavaObscures = true`.
  - `spigot.yml`:
    - `anti-xray.enabled: true`, `engine-mode: 2`, `max-block-height: 320`.
  - **Çalışma Prensibi**: Engine Mode 2, oyuncuya gönderilen paketlerdeki görünmeyen taş ve derin kayrak bloklarının arasına rastgele sahte elmas, zümrüt ve altın blokları yerleştirir. Saydam doku paketi (X-Ray resource pack) açan bir oyuncu baktığında her yeri yüz binlerce sahte elmas olarak görür; gerçek madenleri asla ayırt edemez ve X-Ray tamamen işlevsiz hale gelir.
  - **Panel Entegrasyonu**: Anti-Xray modunu anında yeniden yükleme (`/antixray reload`), aktif/pasif durumunu gösterme ve şüpheli oyuncuların önüne izlenen sahte elmas tuzağı (Honeypot) bırakma butonları.

---

## 3. Değiştirilecek Dosyalar
1. `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\config\antixray.toml`
   - Mod etkinleştirilecek, Engine Mode 2 ve 1.20.1 için 320 blok yüksekliği tanımlanacak.
2. `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\spigot.yml`
   - Spigot anti-xray ayarları Engine Mode 2 ve maksimum cevher listesiyle güncellenecek.
3. `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\admin_panel.py`
   - UI tamamen duyarlı (responsive) sol sidebar + dinamik grid sistemine dönüştürülecek.
   - Casino & Şans Oyunları kategorisi 25+ zengin içerikle baştan sona genişletilecek.
   - Oto-İnşaat kategorisine 25+ yeni mimari eklenecek (Toplam 42+ yapı).
   - Anti-Xray yönetim araçları eklenecek.
