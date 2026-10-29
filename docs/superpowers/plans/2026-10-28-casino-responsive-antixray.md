# Casino, Responsive Panel UI, Mega Yapılar ve Anti-Xray Kalkanı Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Admin panelindeki sekmelerin küçültüldüğünde kaybolmasını responsive sol gezinme menüsüyle çözmek, oyun içine çalışan kollu slot makineleri ve interaktif kumarhane sistemleri eklemek, oto-inşaat kataloğunu 42+ yapıya çıkartmak ve Anti-Xray'i Engine Mode 2 Obfuscation ile kaynak paketlerini körleştirecek şekilde aktif hale getirmek.

**Architecture:** 
1. `config/antixray.toml` ve `spigot.yml` dosyalarında Engine Mode 2 (Obfuscation) yapılandırılır; görünmeyen bloklar sahte cevher paketleriyle donatılır.
2. `admin_panel.py` içindeki `TABS_DATA` tablosuna 25+ yeni interaktif Casino & Şans Oyunu ve 25+ yeni Mega Mimari Yapı şablonu entegre edilir.
3. `admin_panel.py` GUI mimarisi; 24 yatay sekmeden sol tarafta kaydırılabilir ikonlu kategori sidebar'ı, hızlı dropdown seçici ve pencere genişliğine göre 1-3 sütun arasında dinamik uyum sağlayan responsive grid yapısına dönüştürülür.

**Tech Stack:** Python 3 (Tkinter, ttk, threading, socket, struct), TOML, YAML, Minecraft 1.20.1 NBT/Commands & RCON.

**Spec:** `docs/superpowers/specs/2026-10-28-casino-responsive-antixray-design.md`

## Global Constraints
- Python 3.10+ ve Tkinter kütüphaneleriyle uyumlu olmalı, harici 3. parti GUI kütüphanesi (customtkinter vb.) zorunluluğu getirmemeli (mevcut sistem saf Python/Tkinter'dır).
- Minecraft Forge 1.20.1 & Arclight komut sentaksına tam uyumlu olmalı (NBT tagları, item ID'leri, `fill` ve `setblock` sınırları).
- RCON soket bağlantısı kesintisiz ve thread-safe çalışmalı.
- Pencere boyutu minimum `900x650` piksele kadar küçüldüğünde hiçbir sekme, kart veya kontrol butonu kesilmemeli/kaybolmamalıdır.

## Review Focus
- Pencere genişliği 900 piksele düşürüldüğünde buton kartlarının sağa doğru taşmaması ve dikey kaydırmanın sorunsuz çalışması.
- Fare tekerleği (MouseWheel) kaydırmasının yalnızca fare altındaki canvas'ı kaydırması.
- Saydam doku paketi (X-Ray resource pack) kullanan oyuncuların yer altında binlerce sahte elmas ve altın görmesi (Engine Mode 2).
- İnşaat ve Casino komutlarının Minecraft 1.20.1 blok sınırlarını aşmaması ve sunucuda crash yaratmaması.
- RCON komut şablonlarında `{p}` değişkeninin seçili oyuncu veya `@p` ile eksiksiz eşleşmesi.

---

### Task 1: Anti-Xray Yapılandırması ve Obfuscation (Engine Mode 2) Kurulumu

**Files:**
- Modify: `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\config\antixray.toml`
- Modify: `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\spigot.yml`
- Test: `tests/test_antixray_config.py`

- [ ] **Step 1: Write verification test for Anti-Xray configs**
```python
# tests/test_antixray_config.py
import toml
import yaml
import os

SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"

def test_antixray_toml():
    cfg_path = os.path.join(SERVER_DIR, "config", "antixray.toml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = toml.load(f)
    assert data.get("enabled") is True
    assert data["overworld"]["enabled"] is True
    assert data["overworld"]["engineMode"] == 2
    assert data["overworld"]["maxBlockHeight"] >= 320
    assert "diamond_ore" in str(data["overworld"]["hiddenBlocks"]) or "#forge:ores" in data["overworld"]["hiddenBlocks"]

def test_spigot_antixray():
    spigot_path = os.path.join(SERVER_DIR, "spigot.yml")
    with open(spigot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    ax = data["world-settings"]["default"]["anti-xray"]
    assert ax["enabled"] is True
    assert ax["engine-mode"] == 2
    assert ax["max-block-height"] >= 320
```

- [ ] **Step 2: Update `config/antixray.toml` with Engine Mode 2 Obfuscation**
Set `enabled = true` globally, `engineMode = 2` for overworld and the nether, set `maxBlockHeight = 320` for overworld, and add all ores, raw blocks, chests and spawners to hiddenBlocks.

- [ ] **Step 3: Update `spigot.yml` anti-xray block**
Set `anti-xray.enabled: true`, `engine-mode: 2`, `max-block-height: 320`, with comprehensive ore lists.

- [ ] **Step 4: Run test to verify Anti-Xray configuration**
Run: `python -m pytest tests/test_antixray_config.py`
Expected: PASS

---

### Task 2: Casino & Kumarhane Kataloğu Genişletmesi

**Files:**
- Modify: `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\admin_panel.py`
- Test: `tests/test_casino_data.py`

- [ ] **Step 1: Write verification test for Casino items in `admin_panel.py`**
```python
# tests/test_casino_data.py
import admin_panel

def test_casino_category_exists_and_rich():
    items = admin_panel.TABS_DATA.get("🎰 CASİNO & ŞANS OYUNLARI", [])
    assert len(items) >= 20, f"Casino items count is only {len(items)}"
    names = [x[0] for x in items]
    assert any("Slot Makinesi" in n for n in names)
    assert any("Rulet" in n for n in names)
    assert any("Blackjack" in n or "21" in n for n in names)
    assert any("Yazı Tura" in n or "Zar" in n for n in names)
    assert any("Casino" in n and "Palas" in n or "Bina" in n for n in names)
```

- [ ] **Step 2: Implement comprehensive Casino & Gambling templates in `TABS_DATA["🎰 CASİNO & ŞANS OYUNLARI"]`**
Add:
1. 🕹️ Çalışan Kollu 3 Çarklı Slot Makinesi (İn-Game İnşa & Kol Çekmeli)
2. 🏰 Devasa Las Vegas Casino Palas Kompleksi (Işıklı, Lüks Çift Katlı Salon)
3. 🎡 Dev Işıklı Rulet Masası & Bahis Alanı (Kırmızı/Siyah/Yeşil)
4. 🃏 Lüks 21 (Blackjack) Oyun Masası (Dağıtıcı Koltuğu & Çuha)
5. 🪙 Yazı-Tura & Coinflip Düello Standı
6. 🎲 Zar Düellosu & Barbut Masası (1-6 Zar Atışları)
7. 🕵️ Yeraltı Gizli Kumarhanesi (Gizli Kitaplık Girişli)
8. 🎰 Canlı Slot Çevir (Jackpot: 💎 💎 💎 - 50.000 Akçe)
9. 🎰 Canlı Slot Çevir (Mega Kazanç: 7️⃣ 7️⃣ 7️⃣ - 20.000 Akçe)
10. 🎰 Canlı Slot Çevir (Altın Çan: 🔔 🔔 🔔 - 10.000 Akçe)
11. 🎰 Canlı Slot Çevir (Kiraz Bonusu: 🍒 🍒 🍒 - 5.000 Akçe)
12. 🎡 Canlı Rulet Oyna (Kırmızı 32 Kazandı!)
13. 🎡 Canlı Rulet Oyna (Siyah 17 Kazandı!)
14. 🎡 Canlı Rulet Oyna (Yeşil 0 Mega Jackpot!)
15. 🪙 Canlı Yazı Tura (500 Akçe Bahis)
16. 🪙 Canlı Yazı Tura (5.000 Akçe Yüksek Bahis)
17. 🪙 Canlı Yazı Tura (50.000 Akçe VIP Bahis)
18. 🎲 Canlı Çift Zar At (12 Düşeş Geldi!)
19. 🎟️ Sunucu Geneli Büyük Piyango Çekilişi (Tüm Oyunculara Anons)
20. 🎁 Efsanevi Jackpot Şans Kasası (27 Değerli Sürpriz Eşya)
21. 💣 Yüksek Riskli Rus Ruleti Kasası (Troll & Sürpriz)
22. 🏦 Kumarhane Kasa Dairesi & ATM Bankamatiği
23. 👑 VIP Kumarbaz Özel Rütbesi & Parıltılı Başlık
24. 🎆 Görkemli Casino Kutlama Havai Fişekleri

- [ ] **Step 3: Run test to verify Casino items**
Run: `python -m pytest tests/test_casino_data.py`
Expected: PASS

---

### Task 3: Mega Yapı Kataloğu Genişletmesi (Oto-İnşaat 42+ Yapı)

**Files:**
- Modify: `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\admin_panel.py`
- Test: `tests/test_structures_data.py`

- [ ] **Step 1: Write verification test for Mega Structures**
```python
# tests/test_structures_data.py
import admin_panel

def test_structures_count_and_variety():
    items = admin_panel.TABS_DATA.get("🏠 OTO İNŞAAT & EV YAPICI", [])
    assert len(items) >= 40, f"Yapı sayısı {len(items)}, en az 40 olmalı"
    names = [x[0] for x in items]
    assert any("Gökdelen" in n for n in names)
    assert any("Katedral" in n for n in names)
    assert any("Tapınak" in n or "Torii" in n for n in names)
    assert any("Banka" in n or "Kasa" in n for n in names)
    assert any("Stadyum" in n for n in names)
    assert any("Havalimanı" in n for n in names)
    assert any("Kalyon" in n or "Gemi" in n for n in names)
```

- [ ] **Step 2: Add 25+ new iconic structures to `TABS_DATA["🏠 OTO İNŞAAT & EV YAPICI"]`**
Include:
1. 🏙️ 30 Blokluk Modern Cam & Çelik Siber Gökdelen (Panoramik Teraslı, Asansörlü)
2. 🏰 Dev Gotik Katedral & Çan Kulesi (Vitray Camlı, Taş Kemerli)
3. ⛩️ Büyük Japon Torii Tapınağı & Zen Bahçesi (Taş Fenerli, Göletli)
4. 🌊 Atlantis Su Altı Cam Kubbe Şehri (Hava Kilitli, Prizmarin)
5. 🏦 Merkez Bankası & Kırılmaz Çelik Kasa Dairesi (Altın Külçeli, Zırhlı Kapılı)
6. 🏟️ Dev Futbol & Olimpiyat Stadyumu (Tribünlü, Işık Kuleli)
7. 🎡 Lunapark & Işıklı Dönme Dolap (Renkli Yünler, Eğlence Parkı)
8. 🛫 Modern Havalimanı & Işıklı Uçak Pisti (Pist Fenerli, Özel Jetli)
9. ⚓ Dev 3 Direkli Korsan Kalyonu (Yelkenli Savaş Gemisi)
10. 🏯 Büyük Ortaçağ Hanı & Taverna (Şömineli, Ahşap Odalı)
11. 🏎️ Formula 1 Yarış Pisti & Pit Stop (Asfalt Virajlı, Işıklı)
12. 🚀 Uzay Üssü & Roket Fırlatma Rampası (Fütüristik Obsidyen)
13. 🌲 Dev Elf Ağaç Evi (Y: 25 Doğal Merdivenli)
14. 🌴 Tropik Ada Tatil Köyü & Su Bungalovları (İskeleli, Şezlonglu)
15. 🌾 Endüstriyel Dev Çiftlik & Tahıl Siloları (Traktör Maketli)
16. 🕌 Tarihi Kervansaray & Şadırvan (Kemerli Avlu, Su Fıskiyeli)
17. 🧪 Büyük Simya Laboratuvarı & Büyü Kulesi (Kütüphaneli, İmbikli)
18. ❄️ Kutup Araştırma İstasyonu & İglo Köyü (Mavi Buzlu, Çadırlar)
19. 🛸 UFO & Uzaylı İniş Alanı (Neon Işıklar, Çekim Işınlı)
20. 🛡️ Askeri Kışla & Helikopter Pisti (Kamuflaj Çadırlar, Cephanelik)
21. 🌋 Netherite Lav Sarayı & Cehennem Kalesi (Ağlayan Obsidyenli)
22. ⛏️ Mega Taş Ocağı & Madencilik Şantiyesi (Vinçli, Kamyonlu)
23. 🎪 Ortaçağ Sirk Çadırı & Akrobasi Arenası
24. 🏛️ Antik Roma Kolezyumu & Gladyatör Şatosu
25. 🌉 30 Blokluk Işıklı Asma Köprü & Viyadük

- [ ] **Step 3: Run test to verify structure items**
Run: `python -m pytest tests/test_structures_data.py`
Expected: PASS

---

### Task 4: Responsive UI Mimarisi Yenilemesi (Sidebar, Dynamic Grid, No Clipping)

**Files:**
- Modify: `C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server\admin_panel.py`
- Test: `tests/test_panel_ui.py`

- [ ] **Step 1: Write UI tests for responsive layout and event handlers**
```python
# tests/test_panel_ui.py
import admin_panel
import tkinter as tk

def test_admin_gui_initialization():
    root = tk.Tk()
    root.withdraw()
    app = admin_panel.AdminGuiApp(root)
    assert hasattr(app, "sidebar_canvas")
    assert hasattr(app, "content_canvas")
    assert hasattr(app, "category_var")
    assert len(app.category_buttons) >= 24
    root.destroy()
```

- [ ] **Step 2: Refactor UI in `admin_panel.py`**
1. Replace horizontal `ttk.Notebook` with a 2-pane layout:
   - **Sol Sidebar (Kategori Gezgini)**: Genişliği 220px, dikey kaydırılabilir canvas, 24+ kategoriyi butonlar halinde listeler; aktif kategoriyi neon renkle vurgular; kategori arama çubuğu içerir.
   - **Sağ İçerik Alanı**: Seçilen kategorinin butonlarını görüntüler.
2. Dinamik Grid Boyutlandırması (`_on_content_resize`):
   - Sağ panelin anlık piksel genişliğine göre sütun sayısını (Genişlik < 600 ise 1 sütun, 600-950 arası 2 sütun, 950+ ise 3 sütun) otomatik hesaplar.
   - Kartların minimum genişliği esnetilir, böylece pencere ne kadar küçültülürse küçültülsün butonlar asla yatayda kesilmez!
3. MouseWheel Kaydırma Düzeltmesi:
   - Her canvas için `<Enter>` ve `<Leave>` olaylarıyla sadece imlecin altındaki alanın kaydırılması sağlanır.
4. Üst Şerit (Quick Action Ribbon) & Blok Hub:
   - Küçük ekranlarda taşmayı önlemek için esnek `grid` veya 2 satırlı düzenleme yapılır.
5. Anti-Xray Panel Butonları:
   - Anti-Xray reload, durum sorgulama ve Honeypot elmas tuzağı butonları eklenir.

- [ ] **Step 3: Run test to verify UI initialization**
Run: `python -m pytest tests/test_panel_ui.py`
Expected: PASS

---

### Task 5: Entegrasyon Doğrulaması ve Canlı Testler

**Files:**
- Test: `tests/test_integration.py`

- [ ] **Step 1: Run end-to-end integration test**
Verify that all 4 desktop batch files point to the correct files, RCON connects to live server without error, all command templates in TABS_DATA have valid syntax (no missing braces, valid format strings).

- [ ] **Step 2: Test live RCON response**
Send a safe command (`antixray`, `list`) to verify the server handles commands properly.
