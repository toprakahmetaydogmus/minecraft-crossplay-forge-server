# -*- coding: utf-8 -*-
"""
⚔️ MINECRAFT FORGE 1.20.1 ULTIMATE PRO & MASTER CONTROL PANEL
======================================================================
- 🏠 OTO İNŞAAT & EV YAPICI (Auto House & Mega Architecture Builder):
    * Modern Cam & Kuvars Lüks Villa (Havuzlu, Balkonlu, Mobilyalı)
    * Dağ Kütük Evi (Şömineli, Dumanlı Kamp Ateşli, Çatılı, Sandıklı)
    * Ortaçağ Taş Kalesi & Şato (Mazgallı, Kuleli, Fenerli, Zırhlı Kapı)
    * Yeraltı Nükleer / Güvenli Sığınak (Y: -30, Obsidyen Zırhlı, Alarm Lambalı)
    * Otomatik Kızıltaş Hasat Çiftliği (Farmland, Su Akışlı, Hunili, Sandıklı)
    * Modern Gökdelen & Seyir Kulesi (15 Blok Yüksek Cam Kule, Asansör, Teras)
    * Nether Portalı Mabedi (Ağlayan Obsidyen, Altın, Ruh Fenerleri, Lav)
    * Otomatik Maden Asansörü & Şaftı (Y: -58'e Kadar Güvenli İniş ve Merdiven)
    * Gladyatör PvP Arenası (Kumtaşı, Tribünler, Çitler, Meşaleler)
    * 20x20 Arsa Düzleştirici & Alan Temizleyici (Dümdüz Çimen Yapıcı)

- 📦 SİHİRLİ İNŞA SANDIKLARI (Themed Magic Builder Shulker Boxes):
    * Sihirli Villa Sandığı, Dağ Evi Sandığı, Kale & Savunma Sandığı,
      Otomatik Çiftlik Sandığı, Madenci Sandığı, Kızıltaş Fabrika Sandığı,
      Ultimate God Savaşçı Sandığı, Pazar & Ticaret Sandığı

- 💰 AKÇE & EKONOMİ SİSTEMİ (Currency & Banking System):
    * Scoreboard Tabanlı Akçe (Sidebar / Liste / İsim Altı Gösterimi)
    * Anında Bakiye Ekleme / Kesme / Sabitleme (+100 ... +1.000.000 Akçe)
    * Otomatik Maaş Dağıtıcısı (Zamanlayıcı ile Online Oyunculara Periyodik Maaş)
    * 6 Kademeli Fiziksel Para / Külçe Sistemi (Bakır, Gümüş, Altın, Zümrüt, Elmas, Netherite)

- 🏪 MARKET & ÖZEL NPC TÜCCARLAR (Custom Villager Shops & Grand Bazaar):
    * Silah & Zırh Ustası, Mimar & Blokçu, Baş Büyücü & Simyacı,
      Çiftçi & Aşçı, Kızıltaş Mühendisi, Gizli Karaborsacı
    * 11x11 Büyük Ticaret Çarşısı & Pazar Yeri İnşası (4 Tüccar Tezgahı ile)

- ⚡ EFSANEVİ 32K TANRI SETLERİ & EŞYALARI (God Weapons Lvl 255):
    * Kıyamet Kılıcı (Tek Atan), Deprem Kazması, İpeksi Tanrı Kazması,
      Dev Orman Baltası, Nükleer Yay, Makineli Arbalet, Zeus Mızrağı,
      Full Lvl 255 Netherite Zırh Seti, Master Elytra, Aşılmaz Kalkan

- 🪄 BÜYÜ & EFEKT LABORATUVARI (Advanced Enchants & Potion Pharmacy):
    * Eldeki Eşyayı Büyüleme & Özel Seviye Seçimi (1-255)
    * 1-Tıkla Mega Tanrı Buffları & 30+ Özel İksir Efekti

- 🧱 BLOK DAĞITIM MERKEZİ (Universal Block Spawner Hub):
    * 300+ Blok Kataloğu, Serbest ID Girişi, 5 Farklı Yerleştirme Modu

- 🎪 SUNUCU EVENTLERİ & BOSS (Server Events & Minigames):
    * Meteor Yağmuru, Altın & Akçe Yağmuru, Zombi İstilası,
      Boss Arenası (Warden / Wither), Görkemli Havai Fişek Şovu

- 🤡 TROLL & OYUNCU YÖNETİMİ:
    * Zindan, Dondurma, Jumpscarelar, Roket, Örs Bırakma, Envanter Sıfırlama

- 📍 IŞINLANMA & WARP NOKTALARI:
    * Boyutlar, Kayıtlı Spawn, Maden, Market, Arena, Özel X/Y/Z Koordinat Işınlayıcı

- ⚙️ DÜNYA, HAVA & ANTİ-LAG:
    * 1-Tıkla Lag & Çöp Temizliği, TPS Optimizasyonu, Gamerule Kalkanı, Otomatik Kayıt
"""

import os
import sys
import time
import socket
import struct
import threading
import subprocess
import re
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

try:
    import schematics_manager
except Exception as e:
    schematics_manager = None


SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SERVER_DIR, "logs", "latest.log")

def get_server_config():
    """Dynamically loads RCON and Server configuration from server.properties or environment variables."""
    host = os.environ.get("RCON_HOST", "127.0.0.1")
    port = int(os.environ.get("RCON_PORT", "25575"))
    password = os.environ.get("RCON_PASSWORD", "")
    server_port = int(os.environ.get("SERVER_PORT", "25565"))

    props_file = os.path.join(SERVER_DIR, "server.properties")
    if os.path.exists(props_file):
        try:
            with open(props_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k == "rcon.password" and not password:
                        password = v
                    elif k == "rcon.port" and "RCON_PORT" not in os.environ:
                        try:
                            port = int(v)
                        except ValueError:
                            pass
                    elif k == "server-port" and "SERVER_PORT" not in os.environ:
                        try:
                            server_port = int(v)
                        except ValueError:
                            pass
        except Exception:
            pass

    if not password:
        password = "AdminSecurePass123"

    return host, port, password, server_port

RCON_HOST, RCON_PORT, RCON_PASS, SERVER_PORT = get_server_config()

def get_local_ip():
    """Dynamically resolves the active local IP address without any hardcoding."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# =============================================================================
# RCON İSTEMCİSİ (Thread-Safe, Auto-Reconnect)
# =============================================================================
class MinecraftRcon:
    def __init__(self, host=RCON_HOST, port=RCON_PORT, password=RCON_PASS):
        self.host = host
        self.port = port
        self.password = password
        self.sock = None
        self.lock = threading.Lock()

    def connect(self):
        with self.lock:
            try:
                if self.sock:
                    try:
                        self.sock.close()
                    except Exception:
                        pass
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(2.5)
                self.sock.connect((self.host, self.port))
                self._send(3, self.password)
                req_id, resp_type, _ = self._recv()
                if req_id == -1:
                    self.sock.close()
                    self.sock = None
                    return False
                return True
            except Exception:
                self.sock = None
                return False

    def send_command(self, cmd):
        with self.lock:
            if not self.sock:
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.settimeout(2.5)
                    self.sock.connect((self.host, self.port))
                    self._send(3, self.password)
                    req_id, _, _ = self._recv()
                    if req_id == -1:
                        self.sock.close()
                        self.sock = None
                        return "[Hata] RCON şifresi reddedildi."
                except Exception as e:
                    self.sock = None
                    return f"[Bağlantı Yok] Sunucuya bağlanılamadı: {e}"

            try:
                self._send(2, cmd)
                _, _, body = self._recv()
                return body if body.strip() else "[OK] Komut iletildi."
            except Exception as e:
                self.sock = None
                return f"[Hata] Komut iletilemedi: {e}"

    def _send(self, req_type, payload):
        data = payload.encode("utf-8") + b"\x00\x00"
        length = 4 + 4 + len(data)
        pkt = struct.pack("<iii", length, 12345, req_type) + data
        self.sock.sendall(pkt)

    def _recv(self):
        header = self.sock.recv(12)
        if len(header) < 12:
            return -1, 0, ""
        length, req_id, resp_type = struct.unpack("<iii", header)
        remaining = length - 8
        body = b""
        while len(body) < remaining:
            chunk = self.sock.recv(min(4096, remaining - len(body)))
            if not chunk:
                break
            body += chunk
        return req_id, resp_type, body[:-2].decode("utf-8", errors="replace")


# =============================================================================
# SİHİRLİ İNŞAAT & EFSANEVİ SHULKER SANDIKLARI (Güvenli Boyut)
# =============================================================================
CMD_BOX_ARMOR = 'minecraft:give {p} cyan_shulker_box{display:{Name:\'{"text":"🛡️ EFSANEVİ MASTER ZIRH SANDIGI (LVL 255)","color":"aqua","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"netherite_helmet",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"respiration",lvl:255s},{id:"thorns",lvl:255s}]}},{Slot:1b,id:"netherite_chestplate",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"blast_protection",lvl:255s},{id:"thorns",lvl:255s}]}},{Slot:2b,id:"netherite_leggings",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"fire_protection",lvl:255s},{id:"thorns",lvl:255s}]}},{Slot:3b,id:"netherite_boots",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"feather_falling",lvl:255s},{id:"thorns",lvl:255s}]}},{Slot:4b,id:"elytra",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"unbreaking",lvl:255s},{id:"mending",lvl:1s}]}},{Slot:5b,id:"shield",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"unbreaking",lvl:255s},{id:"thorns",lvl:255s}]}}]}} 1'

CMD_BOX_WEAPONS = 'minecraft:give {p} black_shulker_box{display:{Name:\'{"text":"⚡ EFSANEVİ SILAH & ALET SANDIGI","color":"gold","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"netherite_sword",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"sharpness",lvl:255s},{id:"looting",lvl:255s},{id:"fire_aspect",lvl:255s},{id:"sweeping",lvl:255s},{id:"knockback",lvl:10s}]}},{Slot:1b,id:"netherite_pickaxe",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"fortune",lvl:255s}]}},{Slot:2b,id:"netherite_pickaxe",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"silk_touch",lvl:1s}]}},{Slot:3b,id:"netherite_axe",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"sharpness",lvl:255s},{id:"fortune",lvl:255s}]}},{Slot:4b,id:"netherite_shovel",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"fortune",lvl:255s}]}},{Slot:5b,id:"bow",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"power",lvl:255s},{id:"flame",lvl:255s},{id:"punch",lvl:50s},{id:"infinity",lvl:1s}]}},{Slot:6b,id:"crossbow",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"quick_charge",lvl:5s},{id:"multishot",lvl:1s},{id:"piercing",lvl:255s}]}},{Slot:7b,id:"trident",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"impaling",lvl:255s},{id:"loyalty",lvl:3s},{id:"channeling",lvl:1s}]}}]}} 1'

CMD_BOX_SUPPLIES = 'minecraft:give {p} purple_shulker_box{display:{Name:\'{"text":"💎 EFSANEVİ IKMAL SANDIGI","color":"light_purple","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"totem_of_undying",Count:64b},{Slot:1b,id:"totem_of_undying",Count:64b},{Slot:2b,id:"enchanted_golden_apple",Count:64b},{Slot:3b,id:"enchanted_golden_apple",Count:64b},{Slot:4b,id:"firework_rocket",Count:64b,tag:{Fireworks:{Flight:3b}}},{Slot:5b,id:"firework_rocket",Count:64b,tag:{Fireworks:{Flight:3b}}},{Slot:6b,id:"ender_pearl",Count:16b},{Slot:7b,id:"spectral_arrow",Count:64b},{Slot:8b,id:"experience_bottle",Count:64b},{Slot:9b,id:"netherite_block",Count:64b},{Slot:10b,id:"diamond_block",Count:64b},{Slot:11b,id:"golden_carrot",Count:64b}]}} 1'

CMD_COMBO_FULL = f"{CMD_BOX_ARMOR} && {CMD_BOX_WEAPONS} && {CMD_BOX_SUPPLIES}"

# 8 Yeni Sihirli İnşaat Sandığı
CMD_SHULKER_VILLA = 'minecraft:give {p} white_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ VİLLA İNŞA SANDIĞI","color":"aqua","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"smooth_quartz",Count:64b},{Slot:1b,id:"smooth_quartz",Count:64b},{Slot:2b,id:"tinted_glass",Count:64b},{Slot:3b,id:"sea_lantern",Count:64b},{Slot:4b,id:"oak_door",Count:8b},{Slot:5b,id:"red_bed",Count:4b},{Slot:6b,id:"chest",Count:16b},{Slot:7b,id:"water_bucket",Count:4b},{Slot:8b,id:"smooth_stone",Count:64b}]}} 1'

CMD_SHULKER_CABIN = 'minecraft:give {p} brown_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ DAĞ EVİ SANDIĞI","color":"gold","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"spruce_log",Count:64b},{Slot:1b,id:"spruce_planks",Count:64b},{Slot:2b,id:"spruce_stairs",Count:64b},{Slot:3b,id:"glass_pane",Count:64b},{Slot:4b,id:"campfire",Count:8b},{Slot:5b,id:"bricks",Count:64b},{Slot:6b,id:"lantern",Count:32b},{Slot:7b,id:"barrel",Count:16b},{Slot:8b,id:"spruce_door",Count:8b}]}} 1'

CMD_SHULKER_CASTLE = 'minecraft:give {p} gray_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ KALE & SAVUNMA SANDIĞI","color":"dark_gray","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"deepslate_bricks",Count:64b},{Slot:1b,id:"stone_brick_wall",Count:64b},{Slot:2b,id:"iron_bars",Count:64b},{Slot:3b,id:"dispenser",Count:32b},{Slot:4b,id:"arrow",Count:64b},{Slot:5b,id:"lever",Count:16b},{Slot:6b,id:"iron_door",Count:8b},{Slot:7b,id:"sea_lantern",Count:32b},{Slot:8b,id:"tnt",Count:64b}]}} 1'

CMD_SHULKER_FARM = 'minecraft:give {p} green_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ OTOMATİK ÇİFTLİK SANDIĞI","color":"green","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"farmland",Count:64b},{Slot:1b,id:"water_bucket",Count:4b},{Slot:2b,id:"wheat_seeds",Count:64b},{Slot:3b,id:"carrot",Count:64b},{Slot:4b,id:"potato",Count:64b},{Slot:5b,id:"hopper",Count:16b},{Slot:6b,id:"chest",Count:16b},{Slot:7b,id:"bone_meal",Count:64b},{Slot:8b,id:"oak_fence",Count:64b}]}} 1'

CMD_SHULKER_MINE = 'minecraft:give {p} blue_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ MADENCİ & ASANSÖR SANDIĞI","color":"blue","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"netherite_pickaxe",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:5s},{id:"fortune",lvl:3s}]}},{Slot:1b,id:"ladder",Count:64b},{Slot:2b,id:"ladder",Count:64b},{Slot:3b,id:"torch",Count:64b},{Slot:4b,id:"water_bucket",Count:4b},{Slot:5b,id:"soul_sand",Count:16b},{Slot:6b,id:"powered_rail",Count:64b},{Slot:7b,id:"rail",Count:64b},{Slot:8b,id:"chest_minecart",Count:8b}]}} 1'

CMD_SHULKER_REDSTONE = 'minecraft:give {p} red_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ KIZILTAŞ FABRİKA SANDIĞI","color":"red","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"tnt",Count:64b},{Slot:1b,id:"slime_block",Count:64b},{Slot:2b,id:"honey_block",Count:64b},{Slot:3b,id:"sticky_piston",Count:64b},{Slot:4b,id:"observer",Count:64b},{Slot:5b,id:"repeater",Count:64b},{Slot:6b,id:"redstone_block",Count:64b},{Slot:7b,id:"redstone_lamp",Count:64b},{Slot:8b,id:"target",Count:64b}]}} 1'

CMD_SHULKER_ADMIN = 'minecraft:give {p} black_shulker_box{display:{Name:\'{"text":"🧱 FULL ADMİN & İLLEGAL BLOK SANDIĞI","color":"dark_purple","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"barrier",Count:64b},{Slot:1b,id:"command_block",Count:64b},{Slot:2b,id:"repeating_command_block",Count:64b},{Slot:3b,id:"chain_command_block",Count:64b},{Slot:4b,id:"light",Count:64b,tag:{BlockStateTag:{level:"15"}}},{Slot:5b,id:"bedrock",Count:64b},{Slot:6b,id:"spawner",Count:64b},{Slot:7b,id:"structure_block",Count:64b},{Slot:8b,id:"sculk_shrieker",Count:64b,tag:{BlockEntityTag:{can_summon:1b}}}]}} 1'

CMD_SHULKER_MARKET_KIT = 'minecraft:give {p} yellow_shulker_box{display:{Name:\'{"text":"📦 SİHİRLİ TÜCCAR & MARKET SANDIĞI","color":"gold","bold":true}\'},BlockEntityTag:{Items:[{Slot:0b,id:"gold_ingot",Count:64b},{Slot:1b,id:"gold_ingot",Count:64b},{Slot:2b,id:"emerald",Count:64b},{Slot:3b,id:"emerald",Count:64b},{Slot:4b,id:"diamond",Count:64b},{Slot:5b,id:"villager_spawn_egg",Count:16b},{Slot:6b,id:"yellow_wool",Count:64b},{Slot:7b,id:"red_wool",Count:64b},{Slot:8b,id:"barrel",Count:16b}]}} 1'


# =============================================================================
# BLOK DAĞITIM KATALOĞU (Block Catalog)
# =============================================================================
BLOCK_CATALOG = {
    "🔥 EN ÇOK KULLANILANLAR": [
        ("🚫 Görünmez Bariyer Bloğu", "barrier"),
        ("⚡ Standart Komut Bloğu", "command_block"),
        ("🔄 Yineleyici Komut Bloğu", "repeating_command_block"),
        ("⛓️ Zincirleme Komut Bloğu", "chain_command_block"),
        ("💡 Görünmez Işık Bloğu (Işık 15)", "light[level=15]"),
        ("⬛ Kırılamaz Katman Kayası", "bedrock"),
        ("👾 Canavar Spawnerı (Boş)", "spawner"),
        ("🌌 Antik Kalıntı (Ancient Debris)", "ancient_debris"),
        ("🧱 Netherite Bloğu", "netherite_block"),
        ("💎 Elmas Bloğu", "diamond_block"),
        ("🟢 Zümrüt Bloğu", "emerald_block"),
        ("🪙 Altın Bloğu", "gold_block"),
        ("⛓️ Demir Bloğu", "iron_block"),
        ("🌊 Deniz Feneri (Sea Lantern)", "sea_lantern"),
        ("🐸 Sarı Kurbağa Işığı", "ochre_froglight"),
        ("🌸 Kiraz Ağacı Kütüğü", "cherry_log"),
        ("🎋 Bambu Bloğu", "bamboo_block"),
        ("🪟 Karartılmış Cam", "tinted_glass"),
        ("🧊 Mavi Buz", "blue_ice"),
        ("🧨 TNT Bloğu", "tnt")
    ],
    "🧱 İLLEGAL & ADMİN BLOKLARI": [
        ("🚫 Bariyer (Barrier)", "barrier"),
        ("⚡ Komut Bloğu", "command_block"),
        ("🔄 Yineleyici Komut Bloğu", "repeating_command_block"),
        ("⛓️ Zincirleme Komut Bloğu", "chain_command_block"),
        ("💡 Görünmez Işık (Işık 15 - Maks)", "light[level=15]"),
        ("💡 Görünmez Işık (Işık 10 - Orta)", "light[level=10]"),
        ("💡 Görünmez Işık (Işık 5 - Loş)", "light[level=5]"),
        ("⬛ Katman Kayası (Bedrock)", "bedrock"),
        ("🏛️ Yapı Bloğu (Structure Block)", "structure_block"),
        ("🌌 Yapı Boşluğu (Structure Void)", "structure_void"),
        ("🛑 Sınır Bloğu (Border Block)", "border_block"),
        ("🪑 İzin Bloğu (Allow Block)", "allow"),
        ("⛔ Red Bloğu (Deny Block)", "deny"),
        ("👾 Boş Spawner", "spawner"),
        ("🧟 Zombi Spawnerı", 'spawner{BlockEntityTag:{SpawnData:{entity:{id:"minecraft:zombie"}}}}'),
        ("💀 İskelet Spawnerı", 'spawner{BlockEntityTag:{SpawnData:{entity:{id:"minecraft:skeleton"}}}}'),
        ("🔥 Blaze Spawnerı", 'spawner{BlockEntityTag:{SpawnData:{entity:{id:"minecraft:blaze"}}}}'),
        ("🕷️ Örümcek Spawnerı", 'spawner{BlockEntityTag:{SpawnData:{entity:{id:"minecraft:spider"}}}}'),
        ("👹 Aktif Sculk Çığırtkanı (Warden)", 'sculk_shrieker{BlockEntityTag:{can_summon:1b}}'),
        ("🛡️ Güçlendirilmiş Derin Kayrak", "reinforced_deepslate"),
        ("🐉 Ejderha Yumurtası", "dragon_egg"),
        ("👁️ End Portalı Çerçevesi (Gözlü)", "end_portal_frame[eye=true]")
    ],
    "💎 DEĞERLİ MADENLER & CEVHERLER": [
        ("🌌 Antik Kalıntı", "ancient_debris"),
        ("🧱 Netherite Bloğu", "netherite_block"),
        ("💎 Elmas Bloğu", "diamond_block"),
        ("🟢 Zümrüt Bloğu", "emerald_block"),
        ("🪙 Altın Bloğu", "gold_block"),
        ("⛓️ Demir Bloğu", "iron_block"),
        ("🟤 Bakır Bloğu", "copper_block"),
        ("🔴 Kızıltaş Bloğu", "redstone_block"),
        ("🔵 Lapis Lazuli Bloğu", "lapis_block"),
        ("🟣 Ametist Bloğu", "amethyst_block"),
        ("💎 Derin Kayrak Elmas Cevheri", "deepslate_diamond_ore"),
        ("🟢 Derin Kayrak Zümrüt Cevheri", "deepslate_emerald_ore"),
        ("🪙 Derin Kayrak Altın Cevheri", "deepslate_gold_ore"),
        ("⛓️ Derin Kayrak Demir Cevheri", "deepslate_iron_ore")
    ],
    "🏗️ İNŞAAT & MİMARİ BLOKLAR": [
        ("🧱 Derin Kayrak Tuğlası", "deepslate_bricks"),
        ("🧱 Cilalı Derin Kayrak", "polished_deepslate"),
        ("🏛️ Pürüzsüz Kuvars", "smooth_quartz"),
        ("🏛️ Kuvars Sütunu", "quartz_pillar"),
        ("🤍 Kalsit (Calcite)", "calcite"),
        ("🧱 Taş Tuğla", "stone_bricks"),
        ("🧱 Yosunlu Taş Tuğla", "mossy_stone_bricks"),
        ("⬛ Cilalı Kara Taş Tuğlası", "polished_blackstone_bricks"),
        ("🪙 Altın Yaldızlı Kara Taş", "gilded_blackstone"),
        ("🟣 Obsidyen", "obsidian"),
        ("😭 Ağlayan Obsidyen", "crying_obsidian"),
        ("🧊 Mavi Buz", "blue_ice"),
        ("🪟 Karartılmış Cam", "tinted_glass")
    ],
    "💡 AYDINLATMA & IŞIK": [
        ("🏮 Fener (Beacon)", "beacon"),
        ("🌊 Deniz Feneri (Sea Lantern)", "sea_lantern"),
        ("💡 Işıktaşı (Glowstone)", "glowstone"),
        ("🍄 Mantar Işığı (Shroomlight)", "shroomlight"),
        ("🐸 Kehribar Kurbağa Işığı", "ochre_froglight"),
        ("🐸 İnci Kurbağa Işığı", "pearlescent_froglight"),
        ("🐸 Zümrüt Kurbağa Işığı", "verdant_froglight"),
        ("🪄 End Çubuğu (End Rod)", "end_rod"),
        ("🏮 Asılabilir Metal Fener", "lantern"),
        ("💙 Ruh Feneri (Soul Lantern)", "soul_lantern"),
        ("🏕️ Kamp Ateşi", "campfire")
    ]
}


# =============================================================================
# 12 ZENGİN KATEGORİ & 500+ BUTON VERİTABANI
# =============================================================================
TABS_DATA = {
    # -------------------------------------------------------------------------
    # 0. 🚀 OTONOM SUNUCU KURUCU, TÜNELLER & AI MÜHENDİSİ
    # -------------------------------------------------------------------------
    "🚀 OTONOM SUNUCU KURUCU & AI MÜHENDİSİ": [
        ("🚀 Auto Server Maker & AI Suite Aç",
         "__LAUNCH_AUTO_BUILDER__",
         "163+ sürümde otonom sunucu kurucu, Modrinth mod indirici ve AI çökme doktorunu ayrı pencerede açar"),

        ("🌐 Playit.gg Portsuz Tünel Başlat",
         "__LAUNCH_PLAYIT_TUNNEL__",
         "Modem portu açmadan tek tıkla arkadaşlarınızla oynamak için Playit.gg ve UPnP tünellerini yönetir"),

        ("🤖 Yerel AI Çökme Teşhisi (Crash Doctor)",
         "__RUN_CRASH_DOCTOR__",
         "Sunucu loglarını (latest.log) tarar, çakışan modları ve hataları yapay zeka ile teşhis edip açıklar"),

        ("📊 Canlı Donanım Telemetrisi (CPU / RAM)",
         "__SHOW_HARDWARE_METRICS__",
         "İşlemci ve bellek kullanımını gerçek zamanlı konsola yazdırır"),

        ("📦 Modrinth Otomatik Mod İndirici",
         "__LAUNCH_AUTO_BUILDER__",
         "1.20.1 Forge ve diğer tüm sürümler için popüler modları tek tıkla indirip sunucuya kurar"),

        ("☕ Java Ortamı & Sürüm Denetleyicisi",
         "__LAUNCH_AUTO_BUILDER__",
         "Sistemdeki Java sürümlerini tarar, Java 25 çökme korumasını doğrular ve Java 17 çalışma ortamını sağlar")
    ],

    # -------------------------------------------------------------------------
    # 0.1 🏘️ DEV KASABALAR, KÖYLER & ŞEHİRLER (Canlı Köy & Kasaba İnşası)
    # -------------------------------------------------------------------------
    "🏘️ DEV KASABALAR, KÖYLER & ŞEHİRLER": [
        ("🏡 Tam Donanımlı Canlı Ortaçağ Köyü (Meydan, Kilise, Demirci, Çiftlik & Köylüler)",
         "execute at {p} run fill ~-15 ~-1 ~-15 ~15 ~-1 ~15 grass_block && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 smooth_stone && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ bell && execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~1 cobblestone_wall outline && execute at {p} run fill ~-14 ~-1 ~-14 ~-6 ~-1 ~-6 cobblestone && execute at {p} run fill ~-14 ~ ~-14 ~-6 ~3 ~-6 spruce_planks outline && execute at {p} run fill ~-13 ~ ~-13 ~-7 ~2 ~-7 air && execute at {p} run setblock ~-10 ~ ~-10 blast_furnace && execute at {p} run setblock ~-11 ~ ~-10 lava && execute at {p} run setblock ~-9 ~ ~-10 anvil && execute at {p} run summon villager ~-10 ~ ~-8 {VillagerData:{profession:\"weaponsmith\",level:3}} && execute at {p} run fill ~6 ~-1 ~-14 ~14 ~-1 ~-6 farmland && execute at {p} run setblock ~10 ~-1 ~-10 water && execute at {p} run setblock ~10 ~ ~-10 composter && execute at {p} run fill ~7 ~ ~-13 ~13 ~ ~-7 wheat[age=7] && execute at {p} run summon villager ~10 ~ ~-8 {VillagerData:{profession:\"farmer\",level:3}} && execute at {p} run fill ~-14 ~-1 ~6 ~-6 ~-1 ~14 cobblestone && execute at {p} run fill ~-14 ~ ~6 ~-6 ~3 ~14 oak_planks outline && execute at {p} run fill ~-13 ~ ~7 ~-7 ~2 ~13 air && execute at {p} run setblock ~-10 ~ ~10 red_bed && execute at {p} run summon villager ~-9 ~ ~9 {VillagerData:{profession:\"librarian\",level:3}} && execute at {p} run fill ~6 ~-1 ~6 ~14 ~-1 ~14 cobblestone && execute at {p} run fill ~6 ~ ~6 ~14 ~3 ~14 oak_planks outline && execute at {p} run fill ~7 ~ ~7 ~13 ~2 ~13 air && execute at {p} run setblock ~10 ~ ~10 blue_bed && execute at {p} run summon villager ~9 ~ ~9 {VillagerData:{profession:\"cleric\",level:3}} && playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1 && broadcast &a&l[KASABA] &e{p} &adünyaya yaşayan canlı bir &6Ortaçağ Köyü &akuruldu!",
         "Ortasında çanlı köy meydanı, demirci atölyesi, buğday çiftliği, 2 ev ve 4 çalışan usta köylüsüyle 30x30 tam canlı köy"),

        ("🤠 Vahşi Batı Kovboy Kasabası (Saloon, Şerif & Banka)",
         "execute at {p} run fill ~-14 ~-1 ~-8 ~14 ~-1 ~8 coarse_dirt && execute at {p} run fill ~-14 ~-1 ~-6 ~-6 ~-1 ~6 oak_planks && execute at {p} run fill ~-14 ~ ~-6 ~-6 ~4 ~6 oak_planks outline && execute at {p} run fill ~-13 ~ ~-5 ~-7 ~3 ~5 air && execute at {p} run setblock ~-10 ~ ~ barrel && execute at {p} run setblock ~-10 ~ ~1 barrel && execute at {p} run setblock ~-6 ~ ~ oak_fence_gate && execute at {p} run fill ~6 ~-1 ~-6 ~14 ~-1 ~-1 spruce_planks && execute at {p} run fill ~6 ~ ~-6 ~14 ~3 ~-1 spruce_planks outline && execute at {p} run fill ~7 ~ ~-5 ~13 ~2 ~-2 air && execute at {p} run fill ~8 ~ ~-3 ~10 ~1 ~-3 iron_bars && execute at {p} run fill ~6 ~-1 ~1 ~14 ~-1 ~6 smooth_stone && execute at {p} run fill ~6 ~ ~1 ~14 ~3 ~6 smooth_stone outline && execute at {p} run fill ~7 ~ ~2 ~13 ~2 ~5 air && execute at {p} run setblock ~10 ~ ~3 chest && execute at {p} run setblock ~10 ~-1 ~3 gold_block && playsound minecraft:block.wood.place master @a",
         "Saloon meyhanesi, demir parmaklıklı şerif hapishanesi, banka kasası ve toprak ana caddesiyle kovboy kasabası"),

        ("🛡️ Viking Kıyı Köyü & Dev Uzun Ev (Longhouse & Savaş Gemisi)",
         "execute at {p} run fill ~-12 ~-1 ~-6 ~12 ~-1 ~6 spruce_planks && execute at {p} run fill ~-12 ~ ~-6 ~12 ~5 ~6 spruce_log outline && execute at {p} run fill ~-11 ~ ~-5 ~11 ~4 ~5 air && execute at {p} run fill ~-4 ~ ~ ~4 ~ ~ campfire && execute at {p} run fill ~-10 ~ ~-4 ~10 ~ ~-4 barrel && execute at {p} run fill ~-10 ~ ~4 ~10 ~ ~4 barrel && execute at {p} run setblock ~-12 ~1 ~ lantern && execute at {p} run setblock ~12 ~1 ~ lantern && execute at {p} run fill ~-3 ~-2 ~-14 ~3 ~-1 ~-8 dark_oak_planks && execute at {p} run fill ~ ~ ~-12 ~ ~6 ~-12 spruce_log && execute at {p} run fill ~-2 ~3 ~-12 ~2 ~5 ~-12 red_wool && playsound minecraft:item.trident.thunder master {p}",
         "24 blokluk dev ahşap klan ziyafet salonu (Longhouse), ortada ateş ocağı, kalkanlar, fıçılar ve kıyıda yelkenli Viking gemisi"),

        ("🏜️ Çöl Vahası & Bedevi Ticaret Kasabası (Pazar & Palmiyeler)",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 sand && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_sandstone && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 water && execute at {p} run setblock ~-3 ~ ~-3 jungle_sapling && execute at {p} run setblock ~3 ~ ~-3 jungle_sapling && execute at {p} run setblock ~-3 ~ ~3 jungle_sapling && execute at {p} run setblock ~3 ~ ~3 jungle_sapling && execute at {p} run fill ~-10 ~-1 ~-10 ~-5 ~-1 ~-5 cut_sandstone && execute at {p} run fill ~-10 ~ ~-10 ~-5 ~3 ~-5 cut_sandstone outline && execute at {p} run fill ~-9 ~ ~-9 ~-6 ~2 ~-6 air && execute at {p} run fill ~5 ~ ~-8 ~9 ~ ~-8 yellow_wool && execute at {p} run fill ~5 ~ ~-7 ~9 ~ ~-7 red_wool && execute at {p} run setblock ~7 ~ ~-9 chest && execute at {p} run summon villager ~7 ~ ~-7 {VillagerData:{profession:\"cleric\",level:2}}",
         "Ortasında berrak vaha su kaynağı, palmiyeler, kumtaşı evler, rengarenk pazar tenteleri ve tüccarları"),

        ("🌸 Kiraz Çiçeği Geleneksel Japon Kasabası (Torii & Pagodalar)",
         "execute at {p} run fill ~-14 ~-1 ~-14 ~14 ~-1 ~14 dark_prismarine && execute at {p} run fill ~-2 ~-1 ~-14 ~2 ~-1 ~14 gravel && execute at {p} run fill ~-3 ~ ~-12 ~-3 ~5 ~-12 red_concrete && execute at {p} run fill ~3 ~ ~-12 ~3 ~5 ~-12 red_concrete && execute at {p} run fill ~-5 ~5 ~-12 ~5 ~5 ~-12 red_concrete && execute at {p} run fill ~-12 ~-1 ~-4 ~-6 ~-1 ~4 dark_oak_planks && execute at {p} run fill ~-12 ~ ~-4 ~-6 ~4 ~4 stripped_cherry_wood outline && execute at {p} run fill ~-11 ~ ~-3 ~-7 ~3 ~3 air && execute at {p} run fill ~6 ~-1 ~-4 ~12 ~-1 ~4 dark_oak_planks && execute at {p} run fill ~6 ~ ~-4 ~12 ~4 ~4 stripped_cherry_wood outline && execute at {p} run fill ~7 ~ ~-3 ~11 ~3 ~3 air && execute at {p} run setblock ~-4 ~ ~ cherry_sapling && execute at {p} run setblock ~4 ~ ~ cherry_sapling && playsound minecraft:block.cherry_leaves.place master {p}",
         "Büyük kırmızı Torii kapısı, çakıl taşlı cadde, çift taraflı kiraz ahşap pagodalar, fenerler ve kiraz ağaçları"),

        ("🍄 Büyülü Mantar Ormanı Peri Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 mycelium && execute at {p} run fill ~-8 ~ ~-8 ~-4 ~ ~-4 mushroom_stem && execute at {p} run fill ~-9 ~1 ~-9 ~-3 ~3 ~-3 red_mushroom_block outline && execute at {p} run fill ~-8 ~1 ~-8 ~-4 ~2 ~-4 air && execute at {p} run fill ~4 ~ ~-8 ~8 ~ ~-4 mushroom_stem && execute at {p} run fill ~3 ~1 ~-9 ~9 ~3 ~-3 brown_mushroom_block outline && execute at {p} run fill ~4 ~1 ~-8 ~8 ~2 ~-4 air && execute at {p} run setblock ~ ~-1 ~ shroomlight && execute at {p} run setblock ~-6 ~1 ~-6 brewing_stand && execute at {p} run setblock ~6 ~1 ~-6 red_bed && execute at {p} run setblock ~-6 ~1 ~-4 lantern && execute at {p} run setblock ~6 ~1 ~-4 lantern",
         "Miselyum zeminli, dev kırmızı ve kahverengi mantar evler, parıldayan mantar ışıkları, iksir tezgahı peri kasabası"),

        ("⚓ Korsan Koyu & Kaçakçı Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 dark_oak_planks && execute at {p} run fill ~-10 ~ ~-10 ~-4 ~3 ~-4 oak_planks outline && execute at {p} run fill ~-9 ~ ~-9 ~-5 ~2 ~-5 air && execute at {p} run setblock ~-7 ~ ~-7 barrel && execute at {p} run setblock ~-7 ~ ~-6 barrel && execute at {p} run fill ~4 ~ ~-10 ~10 ~6 ~-4 cobblestone outline && execute at {p} run fill ~5 ~ ~-9 ~9 ~5 ~-5 air && execute at {p} run setblock ~7 ~6 ~-7 dispenser[facing=north] && execute at {p} run fill ~-12 ~-1 ~2 ~12 ~-1 ~10 water && execute at {p} run fill ~-2 ~-1 ~2 ~2 ~-1 ~10 dark_oak_slab && execute at {p} run setblock ~ ~ ~4 chest && execute at {p} run setblock ~ ~-1 ~4 gold_block",
         "Ahşap iskeleli, meyhaneli, taş toplu gözetleme kuleli ve gizli altın sandıklı korsan sığınak koyu"),

        ("⚙️ Steampunk Sanayi & Buhar Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 polished_andesite && execute at {p} run fill ~-10 ~ ~-10 ~-4 ~6 ~-4 copper_block outline && execute at {p} run fill ~-9 ~ ~-9 ~-5 ~5 ~-5 air && execute at {p} run setblock ~-7 ~7 ~-7 campfire && execute at {p} run setblock ~-7 ~8 ~-7 cobblestone_wall && execute at {p} run fill ~4 ~ ~-10 ~10 ~8 ~-4 iron_block outline && execute at {p} run fill ~5 ~ ~-9 ~9 ~7 ~-5 air && execute at {p} run setblock ~7 ~ ~-7 blast_furnace && execute at {p} run fill ~-2 ~ ~ ~2 ~ ~ redstone_block && execute at {p} run setblock ~ ~1 ~ observer",
         "Bakır ve demir kaplı atölyeler, duman tüten dev sanayi bacaları, yüksek fırınlar ve kızıltaş güç jeneratörü"),

        ("❄️ Kutup Eskimo & Buzul Araştırma Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 packed_ice && execute at {p} run fill ~-9 ~ ~-9 ~-5 ~3 ~-5 snow_block outline && execute at {p} run fill ~-8 ~ ~-8 ~-6 ~2 ~-6 air && execute at {p} run fill ~5 ~ ~-9 ~9 ~3 ~-5 snow_block outline && execute at {p} run fill ~6 ~ ~-8 ~8 ~2 ~-6 air && execute at {p} run fill ~-9 ~ ~5 ~-5 ~3 ~9 snow_block outline && execute at {p} run fill ~-8 ~ ~6 ~-6 ~2 ~8 air && execute at {p} run setblock ~ ~ ~ campfire && execute at {p} run setblock ~-7 ~ ~-7 white_bed && execute at {p} run setblock ~7 ~ ~-7 blue_bed && execute at {p} run setblock ~-7 ~ ~7 chest",
         "Mavi buz zeminli, 3 adet tam donanımlı kar iglosu, duman tüten kamp ateşi ve kış araştırma sandıkları"),

        ("🌋 Nether Karataş Savunma Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 polished_blackstone && execute at {p} run fill ~-10 ~ ~-10 ~-4 ~4 ~-4 crying_obsidian outline && execute at {p} run fill ~-9 ~ ~-9 ~-5 ~3 ~-5 air && execute at {p} run fill ~4 ~ ~-10 ~10 ~4 ~-4 nether_bricks outline && execute at {p} run fill ~5 ~ ~-9 ~9 ~3 ~-5 air && execute at {p} run setblock ~ ~ ~ respawn_anchor[charges=4] && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 lava && execute at {p} run setblock ~-7 ~1 ~-7 soul_lantern && execute at {p} run setblock ~7 ~1 ~-7 soul_lantern",
         "Ağlayan obsidyen ve karataştan yapılmış zırhlı sığınaklar, lav havuzu, canlanma çapası ve ruh fenerleri"),

        ("🛸 2077 Siberpunk Gelecek Kasabası",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 polished_blackstone && execute at {p} run fill ~-10 ~ ~-10 ~-4 ~6 ~-4 black_concrete outline && execute at {p} run fill ~-9 ~ ~-9 ~-5 ~5 ~-5 air && execute at {p} run fill ~-10 ~2 ~-7 ~-10 ~4 ~-7 light_blue_stained_glass && execute at {p} run fill ~4 ~ ~-10 ~10 ~6 ~-4 black_concrete outline && execute at {p} run fill ~5 ~ ~-9 ~9 ~5 ~-5 air && execute at {p} run fill ~4 ~2 ~-7 ~4 ~4 ~-7 purple_stained_glass && execute at {p} run setblock ~ ~ ~ beacon && execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 emerald_block && execute at {p} run fill ~-2 ~ ~-12 ~2 ~ ~-12 sea_lantern",
         "Siyah beton ve mor/mavi neon camlı siber binalar, merkez lazer feneri ve ışıklı siberpunk cadde"),

        ("🌿 Yeraltı Cüce & Madenci Şehri (Dwarven City)",
         "execute at {p} run fill ~-12 ~-6 ~-12 ~12 ~-1 ~12 deepslate_tiles && execute at {p} run fill ~-11 ~-5 ~-11 ~11 ~-2 ~11 air && execute at {p} run fill ~-8 ~-5 ~-8 ~-8 ~-2 ~-8 deepslate_pillar && execute at {p} run fill ~8 ~-5 ~-8 ~8 ~-2 ~-8 deepslate_pillar && execute at {p} run fill ~-8 ~-5 ~8 ~-8 ~-2 ~8 deepslate_pillar && execute at {p} run fill ~8 ~-5 ~8 ~8 ~-2 ~8 deepslate_pillar && execute at {p} run setblock ~ ~-5 ~ lava && execute at {p} run fill ~-3 ~-5 ~ ~3 ~-5 ~ iron_bars && execute at {p} run setblock ~-6 ~-5 ~-6 chest && execute at {p} run setblock ~6 ~-5 ~-6 anvil",
         "Devasa derin kayrak sütunlu, tavan kemerli, lav eritme ocaklı, örs ve sandıklı yeraltı cüce klan şehri")
    ],

    # -------------------------------------------------------------------------
    # 0.2 🏡 LÜKS EVLER & MALİKANELER (Tüm Tarzlarda Efsanevi Evler)
    # -------------------------------------------------------------------------
    "🏡 LÜKS EVLER & MALİKANELER": [
        ("🏰 3 Katlı Gotik Vampir Malikanesi (Kütüphane & Şömine)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 deepslate_bricks && execute at {p} run fill ~-7 ~ ~-7 ~7 ~14 ~7 deepslate_bricks outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~13 ~6 air && execute at {p} run fill ~-7 ~4 ~-7 ~7 ~4 ~7 dark_oak_planks && execute at {p} run fill ~-7 ~9 ~-7 ~7 ~9 ~7 dark_oak_planks && execute at {p} run fill ~-1 ~4 ~-1 ~1 ~4 ~1 air && execute at {p} run fill ~-1 ~9 ~-1 ~1 ~9 ~1 air && execute at {p} run setblock ~5 ~ ~5 campfire && execute at {p} run setblock ~5 ~1 ~5 bricks && execute at {p} run setblock ~5 ~2 ~5 bricks && execute at {p} run fill ~-5 ~5 ~-5 ~-2 ~5 ~-5 bookshelf && execute at {p} run setblock ~-5 ~10 ~-5 red_bed && execute at {p} run setblock ~ ~1 ~ soul_lantern[hanging=true] && execute at {p} run fill ~-1 ~ ~-7 ~1 ~2 ~-7 air && execute at {p} run setblock ~ ~ ~-7 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-7 iron_door[half=upper,facing=north]",
         "3 katlı taş Gotik köşk, tuğla bacalı şömine, dev kütüphane odası, kırmızı kadife yataklı süit ve zırhlı kapı"),

        ("🌳 Hobbit Çukur Evi (The Shire Yuvarlak Kapılı Doğa Evi)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 dirt && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 dirt && execute at {p} run fill ~-4 ~ ~-4 ~4 ~2 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~4 ~5 grass_block && execute at {p} run fill ~-5 ~ ~-5 ~-5 ~3 ~5 spruce_planks && execute at {p} run setblock ~3 ~ ~3 bricks && execute at {p} run setblock ~3 ~1 ~3 bricks && execute at {p} run setblock ~3 ~2 ~3 campfire && execute at {p} run setblock ~-3 ~ ~-3 green_bed && execute at {p} run setblock ~-3 ~ ~3 barrel && execute at {p} run setblock ~ ~ ~-5 spruce_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 spruce_door[half=upper,facing=north] && execute at {p} run setblock ~ ~2 ~ lantern[hanging=true]",
         "Yemyeşil tepeciğin içine oyulmuş otantik Hobbit çukur evi, çimen çatı, tuğla şömine, fıçılı kiler ve yatak"),

        ("🪵 Lüks İskandinav Dağ Şalesi (A-Frame Üçgen Çatı & Jakuzi)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 dark_oak_planks && execute at {p} run fill ~-6 ~ ~-6 ~6 ~ ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-5 ~1 ~-6 ~5 ~1 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-4 ~2 ~-6 ~4 ~2 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-3 ~3 ~-6 ~3 ~3 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-2 ~4 ~-6 ~2 ~4 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-1 ~5 ~-6 ~1 ~5 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-5 ~ ~-6 ~5 ~4 ~-6 tinted_glass && execute at {p} run fill ~-4 ~ ~-5 ~4 ~3 ~5 air && execute at {p} run fill ~2 ~-1 ~2 ~4 ~-1 ~4 smooth_quartz && execute at {p} run fill ~2 ~ ~2 ~4 ~ ~4 water && execute at {p} run setblock ~-3 ~ ~3 blue_bed && execute at {p} run setblock ~-3 ~ ~ campfire && execute at {p} run setblock ~ ~ ~-6 spruce_door[half=lower,facing=north]",
         "Üçgen A-Frame dik çatılı modern İskandinav dağ evi, boydan boya cam ön cephe, sıcak şömine ve jakuzi havuzu"),

        ("🏯 Geleneksel Japon Minka Çiftçi Evi (Tatami & Bambu Veranda)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 stripped_oak_wood && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 dark_oak_planks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~2 ~4 air && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 hay_block && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 dark_oak_slab && execute at {p} run fill ~-6 ~3 ~-6 ~6 ~3 ~6 dark_oak_stairs[facing=south] outline && execute at {p} run setblock ~ ~ ~-1 bamboo && execute at {p} run setblock ~-3 ~ ~3 red_bed && execute at {p} run setblock ~ ~ ~-5 cherry_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 cherry_door[half=upper,facing=north] && execute at {p} run setblock ~ ~2 ~ lantern",
         "Geleneksel Japon Minka mimarisi, hasır zemin hissi, kavisli saçaklı ahşap çatı, bambu veranda ve fener"),

        ("🌊 Maldivler Su Üstü Cam Bungalov Malikanesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 oak_planks && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 tinted_glass && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 oak_fence outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 hay_block && execute at {p} run setblock ~-3 ~ ~-3 cyan_bed && execute at {p} run setblock ~3 ~ ~-3 chest && execute at {p} run fill ~-1 ~-1 ~-8 ~1 ~-1 ~-5 oak_planks && execute at {p} run setblock ~ ~ ~-1 sea_lantern && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north]",
         "Tabanı okyanus altını gösteren cam zeminli, saman çatılı, iskeleli ve şezlonglu Maldiv su villası"),

        ("🏜️ Modern Çöl Cam Villası (Beyaz Kuvars & Havuzlu Avlu)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_quartz && execute at {p} run fill ~-6 ~ ~-6 ~6 ~4 ~6 smooth_quartz outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-6 ~1 ~-5 ~-6 ~3 ~-2 tinted_glass && execute at {p} run fill ~6 ~1 ~-5 ~6 ~3 ~-2 tinted_glass && execute at {p} run fill ~1 ~-1 ~1 ~4 ~-1 ~4 water && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-4 ~ ~3 white_bed && execute at {p} run setblock ~-4 ~ ~-4 cactus && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Kuvars ve karartılmış camdan avangart çöl villası, avluda gömme yüzme havuzu, kaktüs köşesi ve lüks yatak"),

        ("🍁 Sonbahar Huş Ormanı Çift Katlı Ahşap Evi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 birch_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 stripped_birch_wood outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 birch_planks && execute at {p} run fill ~-1 ~3 ~-1 ~1 ~3 ~1 air && execute at {p} run setblock ~3 ~ ~3 campfire && execute at {p} run setblock ~-3 ~4 ~-3 yellow_bed && execute at {p} run setblock ~3 ~4 ~-3 chest && execute at {p} run setblock ~ ~ ~-5 birch_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 birch_door[half=upper,facing=north]",
         "Huş ağacı kütüklerinden çift katlı sıcacık sonbahar orman evi, şömine, çatı katı yatak odası ve balkon"),

        ("🍄 İki Katlı Kırmızı Mantar Peri Evi",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_stone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~6 ~2 mushroom_stem outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~5 ~1 air && execute at {p} run fill ~-4 ~5 ~-4 ~4 ~7 ~4 red_mushroom_block outline && execute at {p} run fill ~-3 ~5 ~-3 ~3 ~6 ~3 air && execute at {p} run fill ~-1 ~ ~ ~-1 ~5 ~ ladder[facing=east] && execute at {p} run setblock ~ ~5 ~ red_bed && execute at {p} run setblock ~ ~5 ~-2 brewing_stand && execute at {p} run setblock ~ ~ ~-2 oak_door[half=lower,facing=north]",
         "Doğal mantar gövdesi, spiral tırmanma merdiveni, üst katta kırmızı şapka odası, iksir standı ve peri yatağı"),

        ("🧱 Kırsal İngiliz Taş Köy Evi (Tuğla Bacalı Kır Evi)",
         "execute at {p} run fill ~-5 ~-1 ~-4 ~5 ~-1 ~4 cobblestone && execute at {p} run fill ~-5 ~ ~-4 ~5 ~4 ~4 stone_bricks outline && execute at {p} run fill ~-4 ~ ~-3 ~4 ~3 ~3 air && execute at {p} run setblock ~4 ~ ~3 bricks && execute at {p} run setblock ~4 ~1 ~3 bricks && execute at {p} run setblock ~4 ~2 ~3 bricks && execute at {p} run setblock ~4 ~3 ~3 bricks && execute at {p} run setblock ~4 ~4 ~3 campfire && execute at {p} run setblock ~-3 ~ ~2 red_bed && execute at {p} run setblock ~-3 ~ ~1 chest && execute at {p} run setblock ~ ~ ~-4 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-4 oak_door[half=upper,facing=north]",
         "Taş tuğla duvarlı, yüksek tuğla bacasından duman tüten şömineli, nostaljik İngiliz kır evi"),

        ("🛸 Fütüristik Kapsül Minimalist Ev (Cyber Pod)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 iron_block && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run fill ~-4 ~1 ~-3 ~-4 ~2 ~3 light_blue_stained_glass && execute at {p} run fill ~4 ~1 ~-3 ~4 ~2 ~3 light_blue_stained_glass && execute at {p} run setblock ~ ~2 ~ sea_lantern && execute at {p} run setblock ~-2 ~ ~2 white_bed && execute at {p} run setblock ~2 ~ ~2 ender_chest && execute at {p} run fill ~-1 ~ ~-4 ~1 ~1 ~-4 air",
         "Beyaz kuvars ve mavi lazer camdan tek parça aerodinamik kapsül ev, akıllı aydınlatma ve Ender Sandığı"),

        ("🏔️ Uçurum Kenarı Asılı Cam Malikane (Panoramik Teras)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 polished_blackstone && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 smooth_quartz && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-3 ~ ~3 cyan_bed && execute at {p} run setblock ~3 ~ ~3 chest && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north]",
         "Uçurum kenarlarından vadiye uzanan panaromik karartılmış cam zeminli ve tavanlı lüks modern malikane"),

        ("🦇 Yeraltı Gizli Sığınak Malikanesi (Yüzeyde Kulübe, Altta 3 Katlı Lüks Bunker)",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 cobblestone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 spruce_planks outline && execute at {p} run setblock ~ ~ ~ iron_trapdoor && execute at {p} run fill ~ ~-6 ~ ~ ~-1 ~ ladder[facing=north] && execute at {p} run fill ~-5 ~-10 ~-5 ~5 ~-6 ~5 reinforced_deepslate outline && execute at {p} run fill ~-4 ~-9 ~-4 ~4 ~-7 ~4 air && execute at {p} run setblock ~ ~-7 ~ sea_lantern && execute at {p} run setblock ~-3 ~-9 ~-3 enchanting_table && execute at {p} run setblock ~3 ~-9 ~-3 respawn_anchor[charges=4] && execute at {p} run setblock ~-3 ~-9 ~3 red_bed && execute at {p} run setblock ~3 ~-9 ~3 chest",
         "Yüzeyde sıradan küçük kulübe, gizli tuzak kapısından inilen Y:-10 derinliğinde lüks nükleer sığınak malikanesi")
    ],

    "🏢 MEGA PLAZALAR & GÖKDELENLER": [
        ("🏢 35 Katlı Cam & Çelik Siber Plaza (Panoramik Asansör)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~35 ~5 tinted_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~34 ~4 air && execute at {p} run fill ~-5 ~35 ~-5 ~5 ~35 ~5 smooth_quartz && execute at {p} run fill ~-3 ~35 ~-3 ~3 ~35 ~3 yellow_concrete && execute at {p} run setblock ~ ~35 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~34 ~ ladder[facing=north] && execute at {p} run setblock ~-5 ~36 ~-5 sea_lantern && execute at {p} run setblock ~5 ~36 ~-5 sea_lantern && execute at {p} run setblock ~-5 ~36 ~5 sea_lantern && execute at {p} run setblock ~5 ~36 ~5 sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north]",
         "35 blok yüksekliğinde dev kuvars & lazer cam kaplı iş plazası, iç asansör şaftı, çatı helikopter pisti"),

        ("🏬 Grand Alışveriş Plazası & AVM (3 Katlı Mağazalar)",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 smooth_quartz && execute at {p} run fill ~-8 ~ ~-8 ~8 ~12 ~8 smooth_quartz outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~11 ~7 air && execute at {p} run fill ~-8 ~4 ~-8 ~8 ~4 ~8 sea_lantern outline && execute at {p} run fill ~-8 ~8 ~-8 ~8 ~8 ~8 sea_lantern outline && execute at {p} run fill ~-4 ~ ~-8 ~4 ~2 ~-8 tinted_glass && execute at {p} run fill ~-2 ~ ~ ~2 ~ ~ water && execute at {p} run setblock ~ ~1 ~ sea_lantern && execute at {p} run fill ~-6 ~ ~-6 ~-4 ~ ~-4 chest && execute at {p} run fill ~4 ~ ~-6 ~6 ~ ~-4 chest && execute at {p} run fill ~-1 ~ ~-8 ~1 ~2 ~-8 air",
         "3 katlı cam vitrinli lüks AVM plazası, ortada ışıklı süs havuzu, mağaza reyonları ve sandıklar"),

        ("🏙️ İkiz Kuleler / Twin Plaza Towers (Cam Köprü Bağlantılı)",
         "execute at {p} run fill ~-7 ~-1 ~-4 ~-2 ~-1 ~4 polished_blackstone && execute at {p} run fill ~2 ~-1 ~-4 ~7 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-7 ~ ~-4 ~-2 ~25 ~4 tinted_glass outline && execute at {p} run fill ~-6 ~ ~-3 ~-3 ~24 ~3 air && execute at {p} run fill ~2 ~ ~-4 ~7 ~25 ~4 tinted_glass outline && execute at {p} run fill ~3 ~ ~-3 ~6 ~24 ~3 air && execute at {p} run fill ~-2 ~18 ~-1 ~2 ~18 ~1 smooth_quartz && execute at {p} run fill ~-2 ~19 ~-1 ~2 ~20 ~1 glass outline && execute at {p} run fill ~-2 ~19 ~ ~2 ~19 ~ air && execute at {p} run fill ~-5 ~-1 ~ ~-5 ~24 ~ ladder[facing=north] && execute at {p} run fill ~5 ~-1 ~ ~5 ~24 ~ ladder[facing=north]",
         "25 blok yüksekliğinde iki gökdeleni havada 18. katta cam panoramik köprüyle bağlayan dev ikiz kule plazası"),

        ("💎 Wall Street Finans & Uluslararası Borsa Plazası",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 gilded_blackstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~20 ~6 smooth_quartz outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~19 ~5 air && execute at {p} run fill ~-6 ~2 ~-6 ~6 ~18 ~-6 yellow_stained_glass && execute at {p} run fill ~-6 ~2 ~6 ~6 ~18 ~6 yellow_stained_glass && execute at {p} run fill ~-3 ~ ~-3 ~-1 ~ ~-1 gold_block && execute at {p} run fill ~1 ~ ~-3 ~3 ~ ~-1 diamond_block && execute at {p} run setblock ~ ~10 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~19 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Yaldızlı karataş ve kuvars borsa plazası, altın ve elmas işlem katı, tavan fener ışını"),

        ("🏨 5 Yıldızlı Lüks Rezidans & Otel Plazası",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_quartz && execute at {p} run fill ~-6 ~ ~-6 ~6 ~18 ~6 red_concrete outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~17 ~5 air && execute at {p} run fill ~-2 ~ ~-6 ~2 ~ ~-1 red_carpet && execute at {p} run setblock ~ ~ ~-1 lectern[facing=north] && execute at {p} run setblock ~ ~3 ~ sea_lantern && execute at {p} run fill ~-5 ~6 ~-5 ~5 ~6 ~5 oak_planks && execute at {p} run fill ~-5 ~12 ~-5 ~5 ~12 ~5 oak_planks && execute at {p} run setblock ~-3 ~7 ~-3 red_bed && execute at {p} run setblock ~3 ~7 ~-3 blue_bed && execute at {p} run setblock ~-3 ~13 ~-3 yellow_bed && execute at {p} run setblock ~3 ~13 ~-3 green_bed && execute at {p} run fill ~ ~-1 ~ ~ ~17 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Kırmızı halı lobili, resepsiyonlu, süit balkon odalı ve teraslı 5 yıldızlı rezidans plazası"),

        ("🌐 Silikon Vadisi Siber Teknoloji & Yapay Zeka Plazası",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 iron_block && execute at {p} run fill ~-5 ~ ~-5 ~5 ~24 ~5 cyan_stained_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~23 ~4 air && execute at {p} run fill ~-3 ~ ~-3 ~-1 ~ ~-3 target && execute at {p} run fill ~1 ~ ~-3 ~3 ~ ~-3 observer && execute at {p} run fill ~-3 ~ ~3 ~-1 ~ ~3 daylight_detector && execute at {p} run fill ~1 ~ ~3 ~3 ~ ~3 command_block && execute at {p} run setblock ~ ~ ~ conduit && execute at {p} run setblock ~ ~24 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~23 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "Cyan siber cam kaplamalı, yapay zeka sunucu raflı, aktif kanal ve lazer fener kuleli siber plaza"),

        ("🏛️ Büyükşehir Belediye Sarayı & Hükümet Plazası",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 smooth_stone && execute at {p} run fill ~-7 ~ ~-7 ~7 ~14 ~7 smooth_quartz outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~13 ~6 air && execute at {p} run fill ~-6 ~ ~-7 ~-6 ~10 ~-7 quartz_pillar && execute at {p} run fill ~-2 ~ ~-7 ~-2 ~10 ~-7 quartz_pillar && execute at {p} run fill ~2 ~ ~-7 ~2 ~10 ~-7 quartz_pillar && execute at {p} run fill ~6 ~ ~-7 ~6 ~10 ~-7 quartz_pillar && execute at {p} run fill ~-3 ~14 ~-3 ~3 ~14 ~3 gold_block && execute at {p} run fill ~-1 ~ ~-7 ~1 ~2 ~-7 air",
         "Görkemli mermer kuvars sütunlu, altın kubbeli, şehir meclis salonu hükümet plazası"),

        ("🏥 Mega Şehir Hastanesi & Sağlık Plazası (Acil Servis & Heliport)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_stone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~16 ~6 white_concrete outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~15 ~5 air && execute at {p} run fill ~-6 ~6 ~-1 ~-6 ~6 ~1 red_concrete && execute at {p} run fill ~-6 ~5 ~ ~-6 ~7 ~ red_concrete && execute at {p} run fill ~6 ~6 ~-1 ~6 ~6 ~1 red_concrete && execute at {p} run fill ~6 ~5 ~ ~6 ~7 ~ red_concrete && execute at {p} run fill ~-4 ~16 ~-4 ~4 ~16 ~4 yellow_concrete && execute at {p} run fill ~-2 ~16 ~-2 ~2 ~16 ~2 black_concrete && execute at {p} run fill ~ ~-1 ~ ~ ~15 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Kırmızı haç sembollü, acil servisli, çatısında helikopter iniş pisti olan şehir hastanesi plazası"),

        ("⚖️ Adalet Sarayı & Hukuk Kulesi Plazası",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 polished_deepslate && execute at {p} run fill ~-6 ~ ~-6 ~6 ~16 ~6 deepslate_bricks outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~15 ~5 air && execute at {p} run setblock ~ ~ ~ lectern[facing=north] && execute at {p} run setblock ~ ~ ~-1 dark_oak_stairs[facing=south] && execute at {p} run fill ~-4 ~ ~2 ~-2 ~ ~2 dark_oak_fence && execute at {p} run fill ~2 ~ ~2 ~4 ~ ~2 dark_oak_fence && execute at {p} run setblock ~ ~5 ~ sea_lantern && execute at {p} run fill ~-1 ~ ~-6 ~1 ~2 ~-6 air && execute at {p} run setblock ~ ~ ~-6 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-6 iron_door[half=upper,facing=north]",
         "Ağır ceza duruşma salonlu, hakim kürsülü, sanık parmaklıklı adalet sarayı kule plazası"),

        ("🚀 Medya, Radyo & Televizyon Yayın Plazası (Sky TV Tower)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~20 ~3 iron_block outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~19 ~2 air && execute at {p} run fill ~ ~20 ~ ~ ~32 ~ lightning_rod && execute at {p} run fill ~-4 ~20 ~-4 ~4 ~20 ~4 smooth_quartz && execute at {p} run setblock ~-4 ~21 ~-4 sea_lantern && execute at {p} run setblock ~4 ~21 ~-4 sea_lantern && execute at {p} run setblock ~-4 ~21 ~4 sea_lantern && execute at {p} run setblock ~4 ~21 ~4 sea_lantern && execute at {p} run fill ~ ~-1 ~ ~ ~19 ~ ladder[facing=north]",
         "32 blok yüksekliğinde radyo-TV verici antenli, canlı yayın stüdyolu yüksek teknoloji medya plazası"),

        ("🌴 Doğa Dostu Dikey Orman Eko-Plazası (Vertical Forest)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_stone && execute at {p} run fill ~-4 ~ ~-4 ~4 ~22 ~4 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~21 ~3 air && execute at {p} run fill ~-5 ~5 ~-5 ~5 ~5 ~5 oak_leaves && execute at {p} run fill ~-5 ~11 ~-5 ~5 ~11 ~5 oak_leaves && execute at {p} run fill ~-5 ~17 ~-5 ~5 ~17 ~5 oak_leaves && execute at {p} run fill ~-4 ~22 ~-4 ~4 ~22 ~4 grass_block && execute at {p} run setblock ~ ~23 ~ oak_sapling && execute at {p} run fill ~ ~-1 ~ ~ ~21 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-4 ~1 ~1 ~-4 air",
         "Her 5 katta bir dikey teras ormanı ve asılı yaprak bahçeleri olan çevreci gökdelen plazası"),

        ("🛍️ Lüks Moda, Parfüm & Mücevherat Plazası",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~14 ~5 glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~13 ~4 air && execute at {p} run fill ~-5 ~14 ~-5 ~5 ~14 ~5 gold_block && execute at {p} run setblock ~-2 ~ ~-2 armor_stand && execute at {p} run setblock ~2 ~ ~-2 armor_stand && execute at {p} run setblock ~-2 ~ ~2 armor_stand && execute at {p} run setblock ~2 ~ ~2 armor_stand && execute at {p} run setblock ~ ~ ~-1 sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "Vitrin mankenli, altın çatılı, parıltılı cam tasarım lüks moda ve mücevher plazası"),

        ("🏦 Kripto Para & Merkez Bankası Kule Plazası",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 reinforced_deepslate && execute at {p} run fill ~-5 ~ ~-5 ~5 ~18 ~5 iron_block outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~17 ~4 air && execute at {p} run fill ~-3 ~ ~-3 ~-1 ~ ~-1 emerald_block && execute at {p} run fill ~1 ~ ~-3 ~3 ~ ~-1 gold_block && execute at {p} run setblock ~ ~ ~ dispenser[facing=north] && execute at {p} run setblock ~ ~3 ~ sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north]",
         "Güçlendirilmiş zırhlı kasa dairesi, ATM nakit veznesi ve devasa külçe odalı banka kule plazası"),

        ("🛸 2077 Siberpunk Gece Kulübü & Eğlence Plazası",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 polished_blackstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~15 ~6 black_concrete outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~14 ~5 air && execute at {p} run fill ~-6 ~2 ~-6 ~6 ~14 ~-6 purple_stained_glass && execute at {p} run fill ~-6 ~2 ~6 ~6 ~14 ~6 light_blue_stained_glass && execute at {p} run setblock ~ ~ ~ jukebox && execute at {p} run fill ~-2 ~ ~-2 ~2 ~ ~2 sea_lantern && execute at {p} run fill ~ ~-1 ~ ~ ~14 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Mor ve neon mavi ışıklı siberpunk gece kulübü, dans pisti, müzik kutusu ve çatı kokteyl barı"),

        ("🏖️ Marina Sahil Plazası & Lüks Yat Kulübü",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 oak_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~14 ~5 smooth_quartz outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~13 ~4 air && execute at {p} run fill ~-5 ~2 ~-5 ~5 ~12 ~-5 light_blue_stained_glass && execute at {p} run fill ~-6 ~-1 ~-12 ~6 ~-1 ~-7 oak_planks && execute at {p} run fill ~-6 ~ ~-12 ~-6 ~ ~-7 oak_fence && execute at {p} run fill ~6 ~ ~-12 ~6 ~ ~-7 oak_fence && execute at {p} run setblock ~ ~ ~-7 lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "İskele yat limanlı, sahil ahşap yürüyüş yollu, panoramik deniz manzaralı lüks marina plazası")
    ],

    # -------------------------------------------------------------------------
    # 1. OTO İNŞAAT & EV YAPICI (42+ Efsanevi Yapı)
    # -------------------------------------------------------------------------
    "🏠 OTO İNŞAAT & EV YAPICI": [
        ("🏡 2 Katlı Lüks Cam & Havuzlu Villa",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~5 ~5 air && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-5 ~5 ~-5 ~5 ~5 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 air && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-4 ~-1 ~-4 sea_lantern && execute at {p} run setblock ~4 ~-1 ~4 sea_lantern && execute at {p} run setblock ~-3 ~ ~-4 chest && execute at {p} run setblock ~-2 ~ ~-4 crafting_table && execute at {p} run setblock ~-1 ~ ~-4 furnace && execute at {p} run setblock ~-4 ~ ~3 red_bed && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north] && execute at {p} run fill ~-3 ~-2 ~-9 ~3 ~-1 ~-6 smooth_stone && execute at {p} run fill ~-2 ~-2 ~-8 ~2 ~-1 ~-7 water && playsound minecraft:block.anvil.use master {p} ~ ~ ~ 1 1",
         "Kuvars zeminli, cam duvarlı, çift kişilik yataklı, fırınlı ve önünde havuzlu tam modern villa"),

        ("🪵 Dağ Kütük Evi (Şömineli & Bacalı)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 cobblestone && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 spruce_planks outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run fill ~-4 ~ ~-4 ~-4 ~3 ~-4 spruce_log && execute at {p} run fill ~4 ~ ~-4 ~4 ~3 ~-4 spruce_log && execute at {p} run fill ~-4 ~ ~4 ~-4 ~3 ~4 spruce_log && execute at {p} run fill ~4 ~ ~4 ~4 ~3 ~4 spruce_log && execute at {p} run setblock ~3 ~ ~3 bricks && execute at {p} run setblock ~3 ~1 ~3 bricks && execute at {p} run setblock ~3 ~2 ~3 bricks && execute at {p} run setblock ~3 ~3 ~3 campfire && execute at {p} run setblock ~3 ~4 ~3 cobblestone_wall && execute at {p} run setblock ~-3 ~ ~3 blue_bed && execute at {p} run setblock ~-3 ~ ~2 chest && execute at {p} run setblock ~-3 ~ ~1 crafting_table && execute at {p} run setblock ~ ~3 ~ lantern[hanging=true] && execute at {p} run setblock ~ ~ ~-4 spruce_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-4 spruce_door[half=upper,facing=north] && playsound minecraft:block.wood.place master {p} ~ ~ ~ 1 1",
         "Ladin ağacından sıcacık dağ kulübesi, bacasından duman tüten tuğla şömine, yatak ve mobilyalar"),

        ("🏰 Ortaçağ Savunma Şatosu & Kalesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 deepslate_bricks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 air && execute at {p} run fill ~-5 ~ ~-5 ~5 ~5 ~5 deepslate_bricks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-5 ~6 ~-5 ~5 ~6 ~5 stone_brick_wall outline && execute at {p} run setblock ~-5 ~6 ~-5 sea_lantern && execute at {p} run setblock ~5 ~6 ~-5 sea_lantern && execute at {p} run setblock ~-5 ~6 ~5 sea_lantern && execute at {p} run setblock ~5 ~6 ~5 sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~2 ~-5 air && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north] && execute at {p} run setblock ~1 ~ ~-6 stone_button[face=wall,facing=north] && playsound minecraft:block.anvil.place master {p} ~ ~ ~ 1 1",
         "Derin kayraktan aşılmaz kale, mazgallı gözetleme surları, fenerler ve zırhlı demir kapı"),

        ("🛡️ Yeraltı Nükleer / Güvenli Sığınak",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 obsidian && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 reinforced_deepslate outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run fill ~-4 ~4 ~-4 ~4 ~4 ~4 obsidian && execute at {p} run setblock ~ ~3 ~ redstone_lamp && execute at {p} run setblock ~ ~4 ~ redstone_block && execute at {p} run setblock ~-3 ~ ~-3 chest && execute at {p} run setblock ~-2 ~ ~-3 chest && execute at {p} run setblock ~-3 ~ ~3 respawn_anchor[charges=4] && execute at {p} run setblock ~-2 ~ ~3 enchanting_table && execute at {p} run setblock ~-1 ~ ~3 anvil",
         "Patlamaz obsidyen ve güçlendirilmiş derin kayraktan nükleer sığınak, kızıltaş lambaları, örs"),

        ("🌾 Otomatik Kızıltaş Hasat Çiftliği",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 dirt && execute at {p} run fill ~-4 ~ ~-4 ~4 ~2 ~4 air && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 farmland && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ lily_pad && execute at {p} run fill ~-4 ~ ~-4 ~4 ~ ~4 wheat[age=7] && execute at {p} run fill ~-5 ~ ~-5 ~5 ~ ~5 oak_fence outline && execute at {p} run setblock ~ ~ ~-5 oak_fence_gate && execute at {p} run setblock ~-4 ~1 ~-4 torch && execute at {p} run setblock ~4 ~1 ~-4 torch",
         "Su kanallı, çit korumalı, hazır olgunlaşmış buğdaylarla dolu otomatik çiftlik tarlası"),

        ("🏙️ Modern Gökdelen & Seyir Kulesi (15 Blok)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_quartz && execute at {p} run fill ~-3 ~ ~-3 ~3 ~15 ~3 tinted_glass outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~14 ~2 air && execute at {p} run fill ~-3 ~15 ~-3 ~3 ~15 ~3 smooth_quartz && execute at {p} run fill ~-3 ~16 ~-3 ~3 ~16 ~3 glass_pane outline && execute at {p} run setblock ~ ~15 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~14 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-3 ~1 ~1 ~-3 air",
         "15 blok yüksekliğinde panaromik cam gökdelen, iç merdiven şaftı, teras feneri"),

        ("🌋 Nether Geçidi Mabedi",
         "execute at {p} run fill ~-3 ~-1 ~-2 ~3 ~-1 ~2 gilded_blackstone && execute at {p} run fill ~-2 ~ ~ ~2 ~4 ~ obsidian outline && execute at {p} run fill ~-1 ~1 ~ ~1 ~3 ~ nether_portal && execute at {p} run setblock ~-3 ~ ~-2 crying_obsidian && execute at {p} run setblock ~3 ~ ~-2 crying_obsidian && execute at {p} run setblock ~-3 ~ ~2 crying_obsidian && execute at {p} run setblock ~3 ~ ~2 crying_obsidian && execute at {p} run setblock ~-3 ~1 ~-2 soul_lantern && execute at {p} run setblock ~3 ~1 ~-2 soul_lantern && execute at {p} run setblock ~-2 ~-1 ~ gold_block && execute at {p} run setblock ~2 ~-1 ~ gold_block",
         "Yaldızlı karataş, ağlayan obsidyen ve ruh fenerleriyle donatılmış dev aktif Nether kapısı"),

        ("⛏️ Dikey Maden Asansörü (Y: -58'e Kadar)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 -58 ~1 air && execute at {p} run fill ~-2 ~-1 ~-2 ~2 -58 ~2 smooth_stone outline && execute at {p} run fill ~ ~-1 ~ ~ -57 ~ ladder[facing=north] && execute at {p} run setblock ~ ~-58 ~ water && execute at {p} run setblock ~ ~-58 ~1 sea_lantern",
         "Y:-58 elmas katmanına kadar tek tıkla inen merdivenli, aydınlatmalı ve su minderli maden şaftı"),

        ("⚔️ Gladyatör PvP Arenası",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 smooth_sandstone && execute at {p} run fill ~-7 ~ ~-7 ~7 ~3 ~7 air && execute at {p} run fill ~-7 ~ ~-7 ~7 ~ ~7 red_sandstone_wall outline && execute at {p} run setblock ~ ~-1 ~ redstone_block && execute at {p} run setblock ~-7 ~1 ~-7 torch && execute at {p} run setblock ~7 ~1 ~-7 torch && execute at {p} run setblock ~-7 ~1 ~7 torch && execute at {p} run setblock ~7 ~1 ~7 torch",
         "15x15 kumtaşı zeminli, kırmızı duvarlı, dövüşe hazır gladyatör arenası"),

        ("🌱 20x20 Arsa Düzleştirici & Temizleyici",
         "execute at {p} run fill ~-10 ~-1 ~-10 ~10 ~-1 ~10 grass_block && execute at {p} run fill ~-10 ~ ~-10 ~10 ~10 ~10 air && playsound minecraft:block.grass.break master {p} ~ ~ ~ 1 1",
         "Etraftaki tüm engelleri, dağları ve ağaçları silip 20x20 tertemiz yemyeşil inşaat alanı açar"),

        ("🛏️ Acil Durum Gece Barınağı (3x3)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 smooth_stone && execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~1 cobblestone outline && execute at {p} run fill ~ ~ ~ ~ ~1 ~ air && execute at {p} run setblock ~ ~ ~ red_bed && execute at {p} run setblock ~ ~1 ~ torch && execute at {p} run setblock ~ ~ ~-1 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-1 oak_door[half=upper,facing=north]",
         "Gece canavarlarından saniyede korunmak için yataklı ve kapılı anında barınak"),

        ("🏊 7x7 Işıklı Lüks Havuz",
         "execute at {p} run fill ~-3 ~-3 ~-3 ~3 ~-1 ~3 smooth_quartz && execute at {p} run fill ~-2 ~-2 ~-2 ~2 ~-1 ~2 water && execute at {p} run setblock ~ ~-3 ~ sea_lantern",
         "Kuvars çerçeveli, dibinde deniz feneri parlayan berrak serinleme havuzu"),

        ("🏯 Japon Pagoda Tapınağı (Kiraz & Kavisli Çatı)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 dark_oak_planks && execute at {p} run fill ~-4 ~ ~-4 ~4 ~6 ~4 air && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 stripped_cherry_wood outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 air && execute at {p} run fill ~-4 ~3 ~-4 ~4 ~3 ~4 cherry_planks && execute at {p} run fill ~-3 ~4 ~-3 ~3 ~4 ~3 cherry_slab && execute at {p} run setblock ~-4 ~3 ~-4 lantern && execute at {p} run setblock ~4 ~3 ~-4 lantern && execute at {p} run setblock ~-4 ~3 ~4 lantern && execute at {p} run setblock ~4 ~3 ~4 lantern && execute at {p} run setblock ~ ~ ~-3 cherry_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-3 cherry_door[half=upper,facing=north]",
         "Geleneksel Japon kiraz ağacı mimarisi, kavisli saçaklar, asılı fenerler ve meditasyon odası"),

        ("🏜️ Antik Mısır Piramidi & Gizli Hazine Odası",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sandstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~6 ~6 sandstone && execute at {p} run fill ~-5 ~1 ~-5 ~5 ~6 ~5 sandstone && execute at {p} run fill ~-4 ~2 ~-4 ~4 ~6 ~4 sandstone && execute at {p} run fill ~-3 ~3 ~-3 ~3 ~6 ~3 sandstone && execute at {p} run fill ~-2 ~4 ~-2 ~2 ~6 ~2 sandstone && execute at {p} run fill ~-1 ~5 ~-1 ~1 ~6 ~1 sandstone && execute at {p} run setblock ~ ~6 ~ gold_block && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 air && execute at {p} run setblock ~ ~ ~ chest && execute at {p} run setblock ~ ~-1 ~ gold_block && execute at {p} run fill ~ ~ ~-6 ~ ~1 ~-3 air",
         "Zirvesinde altın blok parlayan basamaklı kumtaşı piramit ve içinde gizli sandık mezar odası"),

        ("🌵 Otomatik Kaktüs & Kemik Unu Farmı",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_stone && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 sand && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 glass outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run setblock ~-2 ~ ~-2 cactus && execute at {p} run setblock ~2 ~ ~-2 cactus && execute at {p} run setblock ~-2 ~ ~2 cactus && execute at {p} run setblock ~2 ~ ~2 cactus && execute at {p} run setblock ~-2 ~1 ~-1 iron_bars && execute at {p} run setblock ~2 ~1 ~-1 iron_bars && execute at {p} run setblock ~-2 ~1 ~1 iron_bars && execute at {p} run setblock ~2 ~1 ~1 iron_bars && execute at {p} run setblock ~ ~-1 ~ hopper && execute at {p} run setblock ~ ~-2 ~ chest",
         "Cam korumalı, otomatik kırıcı demir çubuklu, hunili ve sandıklı sonsuz kaktüs hasat mekanizması"),

        ("🛸 Fütüristik Bilimkurgu Cyber Üssü",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 light_blue_stained_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 smooth_quartz && execute at {p} run setblock ~ ~-1 ~ beacon && execute at {p} run setblock ~-4 ~-1 ~-4 sea_lantern && execute at {p} run setblock ~4 ~-1 ~-4 sea_lantern && execute at {p} run setblock ~-4 ~-1 ~4 sea_lantern && execute at {p} run setblock ~4 ~-1 ~4 sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~ ender_chest",
         "Kuvars ve mavi lazer camdan ileri teknoloji sığınak, ortada fener ışını, Ender Sandığı"),

        ("☁️ Gökyüzü Skyblock Adası (Y: 150)",
         "execute at {p} run fill ~-4 148 ~-4 ~4 148 ~4 stone && execute at {p} run fill ~-3 147 ~-3 ~3 147 ~3 dirt && execute at {p} run fill ~-4 149 ~-4 ~4 149 ~4 grass_block && execute at {p} run setblock ~ 150 ~ oak_sapling && execute at {p} run setblock ~-2 150 ~-2 chest && execute at {p} run setblock ~2 150 ~2 water && tp {p} ~ 151 ~",
         "Y:150 irtifada süzülen çimenli Skyblock adası, fidan, sandık ve aşağı dökülen şelale"),

        ("🏙️ 30 Blokluk Modern Siber Gökdelen & Helikopter Pisti",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~30 ~4 tinted_glass outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~29 ~3 air && execute at {p} run fill ~-4 ~30 ~-4 ~4 ~30 ~4 yellow_concrete && execute at {p} run fill ~-2 ~30 ~-2 ~2 ~30 ~2 black_concrete && execute at {p} run setblock ~ ~30 ~ sea_lantern && execute at {p} run fill ~ ~-1 ~ ~ ~29 ~ ladder[facing=north] && execute at {p} run setblock ~-4 ~31 ~-4 lantern && execute at {p} run setblock ~4 ~31 ~-4 lantern && execute at {p} run setblock ~-4 ~31 ~4 lantern && execute at {p} run setblock ~4 ~31 ~4 lantern && execute at {p} run fill ~-1 ~ ~-4 ~1 ~1 ~-4 air",
         "30 blok yüksekliğinde kuvars & karartılmış cam mega gökdelen, terasında helikopter pisti ve asansör"),

        ("🏰 Dev Gotik Katedral & Saat Kulesi",
         "execute at {p} run fill ~-6 ~-1 ~-8 ~6 ~-1 ~8 deepslate_bricks && execute at {p} run fill ~-6 ~ ~-8 ~6 ~12 ~8 deepslate_bricks outline && execute at {p} run fill ~-5 ~ ~-7 ~5 ~11 ~7 air && execute at {p} run fill ~-6 ~2 ~-5 ~-6 ~8 ~-3 purple_stained_glass && execute at {p} run fill ~6 ~2 ~-5 ~6 ~8 ~-3 purple_stained_glass && execute at {p} run fill ~-6 ~2 ~3 ~-6 ~8 ~5 yellow_stained_glass && execute at {p} run fill ~6 ~2 ~3 ~6 ~8 ~5 yellow_stained_glass && execute at {p} run fill ~-3 ~13 ~-3 ~3 ~22 ~3 stone_bricks outline && execute at {p} run fill ~-2 ~13 ~-2 ~2 ~21 ~2 air && execute at {p} run setblock ~ ~18 ~ bell && execute at {p} run setblock ~ ~23 ~ gold_block && execute at {p} run fill ~-1 ~ ~-8 ~1 ~2 ~-8 air",
         "Vitray renkli camlı, yüksek kemerli dev Gotik katedral, tepesinde pirinç çan ve altın haç kulesi"),

        ("⛩️ Büyük Japon Torii Tapınağı & Zen Bahçesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 dark_prismarine && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 coarse_dirt && execute at {p} run fill ~-4 ~ ~-4 ~-4 ~6 ~-4 red_concrete && execute at {p} run fill ~4 ~ ~-4 ~4 ~6 ~-4 red_concrete && execute at {p} run fill ~-6 ~6 ~-4 ~6 ~6 ~-4 red_concrete && execute at {p} run fill ~-5 ~5 ~-4 ~5 ~5 ~-4 red_concrete && execute at {p} run setblock ~-4 ~7 ~-4 lantern && execute at {p} run setblock ~4 ~7 ~-4 lantern && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ lily_pad && execute at {p} run setblock ~-3 ~ ~3 cherry_sapling && execute at {p} run setblock ~3 ~ ~3 cherry_sapling",
         "Görkemli kırmızı Torii kapısı, nilüferli su havuzu, kiraz fidanları ve taş fenerli Zen tapınağı"),

        ("🌊 Atlantis Su Altı Cam Kubbe Şehri",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 prismarine_bricks && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 tinted_glass outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air && execute at {p} run setblock ~ ~-1 ~ conduit && execute at {p} run setblock ~-5 ~-1 ~-5 sea_lantern && execute at {p} run setblock ~5 ~-1 ~-5 sea_lantern && execute at {p} run setblock ~-5 ~-1 ~5 sea_lantern && execute at {p} run setblock ~5 ~-1 ~5 sea_lantern && execute at {p} run setblock ~ ~ ~-6 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-6 iron_door[half=upper,facing=north]",
         "Su altında hava kilitli cam kubbe yaşam alanı, ortasında aktif kanal gücü ve prizmarin zemin"),

        ("🏦 Merkez Bankası & Kırılmaz Çelik Kasa Dairesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_stone && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 iron_block outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-3 ~ ~-3 ~-1 ~ ~-1 gold_block && execute at {p} run fill ~1 ~ ~-3 ~3 ~ ~-1 emerald_block && execute at {p} run fill ~-3 ~ ~1 ~-1 ~ ~3 diamond_block && execute at {p} run fill ~1 ~ ~1 ~3 ~ ~3 netherite_block && execute at {p} run setblock ~ ~3 ~ sea_lantern && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north] && execute at {p} run setblock ~1 ~ ~-6 stone_button[face=wall,facing=north]",
         "Aşılmaz demir zırhlı kasa dairesi, külçe altın/elmas/netherite yığınları ve güvenlik kapısı"),

        ("🏟️ Dev Futbol & Spor Stadyumu",
         "execute at {p} run fill ~-12 ~-1 ~-8 ~12 ~-1 ~8 green_concrete && execute at {p} run fill ~-12 ~ ~-8 ~12 ~3 ~8 air && execute at {p} run fill ~-12 ~-1 ~ ~12 ~-1 ~ white_concrete && execute at {p} run fill ~-12 ~ ~-9 ~12 ~2 ~-9 stone_stairs[facing=south] && execute at {p} run fill ~-12 ~ ~9 ~12 ~2 ~9 stone_stairs[facing=north] && execute at {p} run setblock ~-12 ~1 ~ iron_bars && execute at {p} run setblock ~12 ~1 ~ iron_bars && execute at {p} run setblock ~-11 ~4 ~-8 sea_lantern && execute at {p} run setblock ~11 ~4 ~-8 sea_lantern && execute at {p} run setblock ~-11 ~4 ~8 sea_lantern && execute at {p} run setblock ~11 ~4 ~8 sea_lantern",
         "Yeşil sahalı, orta çizgili, çift kaleli, basamaklı tribünlü ve dev ışık kuleli stadyum kompleksi"),

        ("🎡 Lunapark & Işıklı Dönme Dolap",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_stone && execute at {p} run fill ~ ~ ~ ~ ~10 ~ iron_bars && execute at {p} run fill ~-4 ~5 ~ ~4 ~5 ~ iron_bars && execute at {p} run fill ~ ~1 ~-4 ~ ~1 ~4 iron_bars && execute at {p} run setblock ~-4 ~5 ~ red_wool && execute at {p} run setblock ~4 ~5 ~ blue_wool && execute at {p} run setblock ~ ~9 ~ yellow_wool && execute at {p} run setblock ~ ~1 ~ green_wool && execute at {p} run setblock ~ ~5 ~ sea_lantern && execute at {p} run setblock ~-4 ~6 ~ lantern && execute at {p} run setblock ~4 ~6 ~ lantern",
         "Işıklı demir parmaklık kolları, renkli yün kabinleri ve fenerleriyle dev karnaval dönme dolabı"),

        ("🛫 Modern Havalimanı & Işıklı Uçak Pisti",
         "execute at {p} run fill ~-4 ~-1 ~-15 ~4 ~-1 ~15 polished_blackstone && execute at {p} run fill ~ ~-1 ~-14 ~ ~-1 ~14 yellow_concrete && execute at {p} run fill ~-4 ~-1 ~-14 ~-4 ~-1 ~14 sea_lantern && execute at {p} run fill ~4 ~-1 ~-14 ~4 ~-1 ~14 sea_lantern && execute at {p} run fill ~-4 ~ ~-15 ~4 ~4 ~15 air && execute at {p} run fill ~-2 ~ ~-5 ~2 ~ ~-3 white_wool && execute at {p} run setblock ~ ~1 ~-4 glass",
         "30 blok uzunluğunda çift taraflı deniz feneri ışıklandırmalı kalkış pisti ve özel jet uçağı"),

        ("⚓ Dev 3 Direkli Korsan Kalyonu (Savaş Gemisi)",
         "execute at {p} run fill ~-3 ~-2 ~-8 ~3 ~-1 ~8 dark_oak_planks && execute at {p} run fill ~-3 ~ ~-8 ~3 ~ ~8 dark_oak_fence outline && execute at {p} run fill ~-2 ~ ~-7 ~2 ~ ~7 air && execute at {p} run fill ~ ~ ~-4 ~ ~8 ~-4 spruce_log && execute at {p} run fill ~ ~ ~ ~ ~10 ~ spruce_log && execute at {p} run fill ~ ~ ~4 ~ ~8 ~4 spruce_log && execute at {p} run fill ~-2 ~5 ~-4 ~2 ~7 ~-4 white_wool && execute at {p} run fill ~-2 ~6 ~ ~2 ~9 ~ white_wool && execute at {p} run fill ~-2 ~5 ~4 ~2 ~7 ~4 white_wool && execute at {p} run setblock ~-3 ~ ~ dispenser[facing=west] && execute at {p} run setblock ~3 ~ ~ dispenser[facing=east]",
         "Koyu meşe gövdeli, 3 beyaz yelkenli yüksek direkli, borda toplu dev deniz savaş kalyonu"),

        ("🏯 Büyük Ortaçağ Hanı & Taverna (The Prancing Pony)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 spruce_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 oak_planks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 spruce_planks && execute at {p} run fill ~-1 ~3 ~-1 ~1 ~3 ~1 air && execute at {p} run setblock ~4 ~ ~4 campfire && execute at {p} run setblock ~4 ~1 ~4 cobblestone_wall && execute at {p} run setblock ~-3 ~ ~3 barrel && execute at {p} run setblock ~-3 ~ ~2 barrel && execute at {p} run setblock ~-3 ~4 ~3 red_bed && execute at {p} run setblock ~3 ~4 ~3 blue_bed && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north]",
         "Çift katlı ahşap han, alt katta şömine ve fıçılı taverna, üst katta misafir yatak odaları"),

        ("🏎️ Formula 1 Yarış Pisti & Pit Stop",
         "execute at {p} run fill ~-5 ~-1 ~-10 ~5 ~-1 ~10 polished_blackstone && execute at {p} run fill ~-5 ~-1 ~-10 ~-5 ~-1 ~10 red_concrete && execute at {p} run fill ~5 ~-1 ~-10 ~5 ~-1 ~10 white_concrete && execute at {p} run fill ~-4 ~-1 ~ ~4 ~-1 ~ white_concrete && execute at {p} run setblock ~-4 ~1 ~ redstone_lamp && execute at {p} run setblock ~-4 ~2 ~ redstone_block && execute at {p} run setblock ~4 ~1 ~ redstone_lamp && execute at {p} run setblock ~4 ~2 ~ redstone_block",
         "Kırmızı-beyaz yarış bordürlü, siyah asfalt zeminli, kalkış ışıklı Formula 1 pisti düzlüğü"),

        ("🚀 Uzay Üssü & Roket Fırlatma Rampası",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 iron_block && execute at {p} run fill ~-1 ~ ~-1 ~1 ~12 ~1 white_concrete && execute at {p} run fill ~ ~13 ~ ~ ~15 ~ orange_concrete && execute at {p} run setblock ~ ~16 ~ red_concrete && execute at {p} run fill ~-3 ~ ~-3 ~-3 ~15 ~-3 iron_bars && execute at {p} run setblock ~ ~-1 ~ campfire && execute at {p} run setblock ~-4 ~ ~-4 sea_lantern && execute at {p} run setblock ~4 ~ ~-4 sea_lantern && execute at {p} run setblock ~-4 ~ ~4 sea_lantern && execute at {p} run setblock ~4 ~ ~4 sea_lantern",
         "Fırlatma iskelesi, duman püskürten kamp ateşi ve 16 blok yüksekliğinde Saturn uzay roketi"),

        ("🌲 Dev Elf Ağaç Evi (Y: 25 Yüksek)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~20 ~1 oak_log && execute at {p} run fill ~ ~-1 ~-2 ~ ~20 ~-2 ladder[facing=north] && execute at {p} run fill ~-5 20 ~-5 ~5 20 ~5 oak_planks && execute at {p} run fill ~-6 21 ~-6 ~6 21 ~6 oak_leaves outline && execute at {p} run fill ~-5 24 ~-5 ~5 24 ~5 oak_leaves && execute at {p} run setblock ~-4 21 ~-4 lantern && execute at {p} run setblock ~4 21 ~-4 lantern && execute at {p} run setblock ~-4 21 ~4 lantern && execute at {p} run setblock ~4 21 ~4 lantern && execute at {p} run setblock ~ 21 ~2 red_bed && execute at {p} run setblock ~-2 21 ~2 chest",
         "20 blok yüksekliğinde dev meşe gövdesi, tepeye çıkan merdiven, yaprak çatılı teras ve yatak odası"),

        ("🌴 Tropik Ada Tatil Köyü & Su Bungalovları",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sand && execute at {p} run fill ~-2 ~ ~-2 ~2 ~ ~2 oak_planks && execute at {p} run fill ~-2 ~1 ~-2 ~2 ~3 ~2 oak_fence outline && execute at {p} run fill ~-3 ~4 ~-3 ~3 ~4 ~3 hay_block && execute at {p} run setblock ~ ~1 ~ yellow_bed && execute at {p} run setblock ~-5 ~ ~-5 jungle_sapling && execute at {p} run setblock ~5 ~ ~5 jungle_sapling && execute at {p} run setblock ~ ~1 ~-3 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~2 ~-3 oak_door[half=upper,facing=north]",
         "Saman çatılı lüks sahil bungalovu, palmiyeler, sarı dinlenme yatağı ve kumsal"),

        ("🌾 Endüstriyel Dev Çiftlik & Tahıl Siloları",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_stone && execute at {p} run fill ~-4 ~ ~-4 ~-2 ~8 ~-2 smooth_quartz outline && execute at {p} run fill ~-4 ~ ~2 ~-2 ~8 ~4 smooth_quartz outline && execute at {p} run fill ~2 ~ ~-4 ~5 ~4 ~4 red_concrete outline && execute at {p} run fill ~3 ~ ~-3 ~4 ~3 ~3 air && execute at {p} run fill ~-3 ~ ~-3 ~-3 ~6 ~-3 hay_block && execute at {p} run fill ~-3 ~ ~3 ~-3 ~6 ~3 hay_block && execute at {p} run setblock ~2 ~ ~ oak_door[half=lower,facing=west] && execute at {p} run setblock ~2 ~1 ~ oak_door[half=upper,facing=west]",
         "8 blok yüksekliğinde çift silolu tahıl deposu, saman balyaları ve kırmızı ahşap çiftlik ambarı"),

        ("🕌 Tarihi Kervansaray & Şadırvan",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sandstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~3 ~6 cut_sandstone outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 smooth_quartz && execute at {p} run setblock ~ ~ ~ water && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-5 ~1 ~-5 soul_lantern && execute at {p} run setblock ~5 ~1 ~-5 soul_lantern && execute at {p} run setblock ~-5 ~1 ~5 soul_lantern && execute at {p} run setblock ~5 ~1 ~5 soul_lantern && execute at {p} run fill ~-1 ~ ~-6 ~1 ~2 ~-6 air",
         "Selçuklu & Osmanlı tarzı kumtaşı kervansaray avlusu, ortada parıldayan şadırvan havuzu"),

        ("🧪 Büyük Simya Laboratuvarı & Büyü Kulesi",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 obsidian && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 polished_blackstone outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 air && execute at {p} run fill ~-3 ~ ~-3 ~3 ~1 ~3 bookshelf outline && execute at {p} run setblock ~ ~ ~ enchanting_table && execute at {p} run setblock ~-2 ~ ~ brewing_stand && execute at {p} run setblock ~2 ~ ~ cauldron && execute at {p} run setblock ~ ~4 ~ beacon && execute at {p} run setblock ~ ~-1 ~ netherite_block && execute at {p} run fill ~-1 ~ ~-4 ~1 ~1 ~-4 air",
         "Kütüphane rafları, seviye 30 büyü masası, iksir imbikleri, kazanlar ve tavanda aktif fener"),

        ("❄️ Kutup Araştırma İstasyonu & İglo Köyü",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 packed_ice && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 snow_block outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 air && execute at {p} run setblock ~ ~ ~ campfire && execute at {p} run setblock ~-2 ~ ~2 white_bed && execute at {p} run setblock ~2 ~ ~2 chest && execute at {p} run setblock ~ ~ ~-3 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-3 iron_door[half=upper,facing=north] && execute at {p} run setblock ~-3 ~3 ~-3 lantern && execute at {p} run setblock ~3 ~3 ~-3 lantern",
         "Buz tabanlı sıcak kar iglosu, dumanlı kamp ateşi, beyaz kutup yatağı ve ikmal sandığı"),

        ("🛸 UFO & Uzaylı İniş Alanı",
         "execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 smooth_stone && execute at {p} run fill ~-3 ~5 ~-3 ~3 ~5 ~3 lime_stained_glass && execute at {p} run setblock ~ ~3 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~2 ~ lime_stained_glass && execute at {p} run setblock ~-4 ~4 ~-4 sea_lantern && execute at {p} run setblock ~4 ~4 ~-4 sea_lantern && execute at {p} run setblock ~-4 ~4 ~4 sea_lantern && execute at {p} run setblock ~4 ~4 ~4 sea_lantern",
         "Gökyüzünde süzülen uçan daire diski, yeşil cam kokpiti, lazer çekim ışını ve neon ışıklar"),

        ("🛡️ Askeri Kışla & Helikopter Pisti",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 coarse_dirt && execute at {p} run fill ~-5 ~ ~-5 ~-1 ~2 ~-1 green_wool outline && execute at {p} run fill ~-4 ~ ~-4 ~-2 ~1 ~-2 air && execute at {p} run fill ~1 ~-1 ~1 ~5 ~-1 ~5 polished_blackstone && execute at {p} run setblock ~3 ~-1 ~3 yellow_concrete && execute at {p} run fill ~1 ~-1 ~3 ~5 ~-1 ~3 yellow_concrete && execute at {p} run fill ~3 ~-1 ~1 ~3 ~-1 ~5 yellow_concrete && execute at {p} run setblock ~-3 ~ ~-2 chest && execute at {p} run setblock ~-3 ~ ~-3 green_bed",
         "Kamuflaj askeri çadır, silah ve cephane sandıkları, yan tarafında sarı 'H' helikopter iniş pisti"),

        ("🌋 Netherite Lav Sarayı & Cehennem Kalesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 netherite_block && execute at {p} run fill ~-5 ~ ~-5 ~5 ~5 ~5 crying_obsidian outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 air && execute at {p} run setblock ~-3 ~3 ~-3 lava && execute at {p} run setblock ~3 ~3 ~-3 lava && execute at {p} run setblock ~-3 ~3 ~3 lava && execute at {p} run setblock ~3 ~3 ~3 lava && execute at {p} run setblock ~ ~ ~ respawn_anchor[charges=4] && execute at {p} run fill ~-1 ~ ~-5 ~1 ~2 ~-5 air",
         "Ağlayan obsidyen ve netherite bloklarından dev kale, 4 köşeden akan lav şelaleleri ve canlanma çapası"),

        ("⛏️ Mega Taş Ocağı & Madencilik Şantiyesi",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 cobblestone && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-3 ~4 air && execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 stone_brick_wall outline && execute at {p} run fill ~-4 ~ ~ ~4 ~ ~ powered_rail && execute at {p} run setblock ~ ~ ~ chest_minecart && execute at {p} run setblock ~-3 ~ ~2 tnt && execute at {p} run setblock ~-3 ~ ~3 tnt",
         "Kazı çukurlu, taş duvar korumalı, elektrikli raylı vagon sistemi ve patlayıcı TNT istasyonu"),

        ("🎪 Ortaçağ Sirk Çadırı & Akrobasi Arenası",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 coarse_dirt && execute at {p} run fill ~-5 ~ ~-5 ~5 ~ ~5 red_wool outline && execute at {p} run fill ~-4 ~1 ~-4 ~4 ~1 ~4 white_wool outline && execute at {p} run fill ~-3 ~2 ~-3 ~3 ~2 ~3 red_wool outline && execute at {p} run fill ~-2 ~3 ~-2 ~2 ~3 ~2 white_wool outline && execute at {p} run fill ~-1 ~4 ~-1 ~1 ~4 ~1 red_wool outline && execute at {p} run setblock ~ ~5 ~ yellow_wool && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "Kırmızı-beyaz çizgili kubbeli sirk çadırı, gösteri arenası ve bayrak direği"),

        ("🏛️ Antik Roma Kolezyumu & Gladyatör Şatosu",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 sandstone && execute at {p} run fill ~-8 ~ ~-8 ~8 ~3 ~8 smooth_sandstone outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~ ~7 sandstone_stairs[facing=south] && execute at {p} run fill ~-6 ~1 ~-6 ~6 ~1 ~6 sandstone_stairs[facing=south] && execute at {p} run fill ~-5 ~ ~-5 ~5 ~2 ~5 air && execute at {p} run setblock ~ ~-1 ~ redstone_block && execute at {p} run setblock ~-8 ~4 ~-8 torch && execute at {p} run setblock ~8 ~4 ~-8 torch && execute at {p} run setblock ~-8 ~4 ~8 torch && execute at {p} run setblock ~8 ~4 ~8 torch",
         "Basamaklı taş seyirci tribünleri, dövüş arenası ve meşaleli yüksek surlarıyla Roma Kolezyumu"),

        ("🌉 30 Blokluk Işıklı Asma Köprü & Viyadük",
         "execute at {p} run fill ~-2 ~-1 ~-15 ~2 ~-1 ~15 deepslate_brick_slab && execute at {p} run fill ~-2 ~ ~-15 ~-2 ~ ~15 deepslate_brick_wall && execute at {p} run fill ~2 ~ ~-15 ~2 ~ ~15 deepslate_brick_wall && execute at {p} run setblock ~-2 ~1 ~-10 lantern && execute at {p} run setblock ~2 ~1 ~-10 lantern && execute at {p} run setblock ~-2 ~1 ~ lantern && execute at {p} run setblock ~2 ~1 ~ lantern && execute at {p} run setblock ~-2 ~1 ~10 lantern && execute at {p} run setblock ~2 ~1 ~10 lantern",
         "30 blok uzunluğunda kanyonları ve nehirleri bağlayan derin kayrak taşlı, fenerli asma köprü")
    ],

    # -------------------------------------------------------------------------
    # 2. SİHİRLİ İNŞA SANDIKLARI
    # -------------------------------------------------------------------------
    "📦 SİHİRLİ İNŞA SANDIKLARI": [
        ("📦 Sihirli Villa Sandığı", CMD_SHULKER_VILLA, "Kuvars, Karartılmış Cam, Deniz Feneri, Meşe Kapılar, Su Kovası, Yatak, Sandık"),
        ("📦 Sihirli Dağ Evi Sandığı", CMD_SHULKER_CABIN, "Ladin Kütükleri, Tahtalar, Merdivenler, Şömine Tuğlaları, Kamp Ateşi, Fenerler"),
        ("📦 Sihirli Kale & Savunma Sandığı", CMD_SHULKER_CASTLE, "Derin Kayrak Tuğlası, Duvarlar, Demir Parmaklıklar, Fırlatıcılar, Oklar, TNT"),
        ("📦 Sihirli Otomatik Çiftlik Sandığı", CMD_SHULKER_FARM, "Tarla Bloğu, Su Kovaları, Tohumlar, Havuç, Patates, Huniler, Sandıklar, Kemik Tozu"),
        ("📦 Sihirli Madenci & Asansör Sandığı", CMD_SHULKER_MINE, "God Kazma, 128x Merdiven, 64x Meşale, Ruh Kumu, Güçlendirilmiş Raylar, Vagonlar"),
        ("📦 Sihirli Kızıltaş Fabrika Sandığı", CMD_SHULKER_REDSTONE, "TNT, Balçık, Bal Blokları, Yapışkan Pistonlar, Gözlemciler, Kızıltaş Blokları, Hedef"),
        ("📦 Full Admin & İllegal Blok Sandığı", CMD_SHULKER_ADMIN, "Bariyer, Komut Blokları, Görünmez Işık 15, Bedrock, Spawner, Sculk Shrieker"),
        ("📦 Sihirli Tüccar & Pazar Sandığı", CMD_SHULKER_MARKET_KIT, "Altın Külçeler, Zümrütler, Elmaslar, Köylü Yumurtaları, Renkli Yünler, Variller")
    ],

    # -------------------------------------------------------------------------
    # 3. AKÇE & EKONOMİ SİSTEMİ
    # -------------------------------------------------------------------------
    "💰 AKÇE & EKONOMİ SİSTEMİ": [
        ("💰 [Kutudaki Miktarı] Yükle (+{akce} Akçe)", "eco give {p} {akce} && scoreboard players add {p} akce {akce} && title {p} actionbar {\"text\":\"💰 +{akce} Akçe Yüklendi!\",\"color\":\"green\"}", "Üst şeritteki 'Akçe' kutusuna yazdığınız özel miktarı oyuncuya yükler"),
        ("💸 [Kutudaki Miktarı] Kes (-{akce} Akçe)", "eco take {p} {akce} && scoreboard players remove {p} akce {akce} && title {p} actionbar {\"text\":\"💸 -{akce} Akçe Kesildi!\",\"color\":\"red\"}", "Üst şeritteki 'Akçe' kutusuna yazdığınız özel miktarı oyuncudan keser"),
        ("🎯 Bakiyeyi [Kutudaki Miktara] Sabitle ({akce} Akçe)", "eco set {p} {akce} && scoreboard players set {p} akce {akce} && title {p} actionbar {\"text\":\"🎯 Bakiye: {akce} Akçe Olarak Güncellendi!\",\"color\":\"gold\"}", "Oyuncunun bakiyesini tam olarak kutudaki miktara eşitler"),

        ("🪙 Akçe Sistemini Kur & Başlat",
         "scoreboard objectives add akce dummy {\"text\":\"✦ AKÇE ✦\",\"color\":\"gold\",\"bold\":true} && eco give {p} 1000 && scoreboard players add {p} akce 1000 && title {p} title {\"text\":\"🪙 AKÇE SİSTEMİ DEVREDE!\",\"color\":\"gold\",\"bold\":true} && title {p} subtitle {\"text\":\"1.000 Akçe Başlangıç Bakiyesi Yüklendi\",\"color\":\"yellow\"} && playsound minecraft:entity.player.levelup master {p}",
         "Scoreboard ve Vault ekonomisini eşitler, sağ taraftaki paneli ve marketi 1000 akçe ile başlatır"),

        ("👁️ Akçeyi Yan Ekranda Göster (Sidebar)", "scoreboard objectives setdisplay sidebar akce", "Ekranın sağındaki skor tablosunda gösterir"),
        ("📋 Akçeyi Oyuncu Listesinde Göster (Tab)", "scoreboard objectives setdisplay list akce", "Tab tuşuna basınca oyuncunun yanında gösterir"),
        ("👤 Akçeyi Oyuncu İsminin Altında Göster", "scoreboard objectives setdisplay belowName akce", "Oyuncunun kafasının üzerinde gösterir"),
        ("🙈 Yan Skor Tablosunu Aç/Kapat (/sb)", "tab scoreboard toggle {p}", "Sağdaki skor tablosunu ekranda açar veya gizler"),

        ("💰 +100 Akçe Yükle (Market & Skor)", "eco give {p} 100 && scoreboard players add {p} akce 100 && playsound minecraft:entity.experience_orb.pickup master {p}", "Hem /shop hem de sağ skor tablosuna anında 100 Akçe ekler"),
        ("💰 +500 Akçe Yükle (Market & Skor)", "eco give {p} 500 && scoreboard players add {p} akce 500 && playsound minecraft:entity.experience_orb.pickup master {p}", "Hem /shop hem de sağ skor tablosuna anında 500 Akçe ekler"),
        ("💰 +1.000 Akçe Yükle (Market & Skor)", "eco give {p} 1000 && scoreboard players add {p} akce 1000 && playsound minecraft:entity.player.levelup master {p}", "Hem /shop hem de sağ skor tablosuna anında 1.000 Akçe yükler"),
        ("💰 +10.000 Akçe Yükle (Market & Skor)", "eco give {p} 10000 && scoreboard players add {p} akce 10000 && playsound minecraft:entity.player.levelup master {p}", "Hem /shop hem de sağ skor tablosuna anında 10.000 Akçe yükler"),
        ("💰 +100.000 Akçe Milyarder Yüklemesi", "eco give {p} 100000 && scoreboard players add {p} akce 100000 && title {p} title {\"text\":\"💎 MİLYARDER OLDUNUZ!\",\"color\":\"aqua\",\"bold\":true}", "Hem /shop marketine hem sağ tabloya 100.000 Akçe anında yükler"),
        ("💰 +1.000.000 İmparatorluk Hazinesi", "eco give {p} 1000000 && scoreboard players add {p} akce 1000000 && title {p} title {\"text\":\"👑 İMPARATORLUK HAZİNESİ!\",\"color\":\"gold\",\"bold\":true}", "Hem /shop marketine hem sağ tabloya 1 Milyon Akçe hazine aktarır"),

        ("🔄 Bakiyeyi 100.000 Yap (Senkronize Eşitle)", "eco set {p} 100000 && scoreboard players set {p} akce 100000 && tellraw {p} [{\"text\":\"[BANKA]: \",\"color\":\"gold\",\"bold\":true},{\"text\":\"Bakiyeniz 100.000 Akçe olarak eşitlendi!\",\"color\":\"green\"}]", "Sağ tablo ve /shop market bakiyesini tam 100.000 Akçeye eşitler"),
        ("🔄 Bakiyeyi 1.000.000 Yap (Senkronize Eşitle)", "eco set {p} 1000000 && scoreboard players set {p} akce 1000000 && tellraw {p} [{\"text\":\"[BANKA]: \",\"color\":\"gold\",\"bold\":true},{\"text\":\"Bakiyeniz 1.000.000 Akçe olarak eşitlendi!\",\"color\":\"green\"}]", "Sağ tablo ve /shop market bakiyesini tam 1 Milyon Akçeye eşitler"),

        ("💸 -500 Akçe Kes (Vergi/Harcama)", "eco take {p} 500 && scoreboard players remove {p} akce 500", "Hem marketten hem sağ tablodan 500 Akçe keser"),
        ("💸 -5.000 Akçe Ceza Kes", "eco take {p} 5000 && scoreboard players remove {p} akce 5000", "Hem marketten hem sağ tablodan 5.000 Akçe ceza keser"),
        ("🔄 Akçeyi Sıfırla (0 Yap)", "eco set {p} 0 && scoreboard players set {p} akce 0", "Hesaptaki tüm akçeyi silip sıfırlar"),
        ("📜 Bakiye Raporu Ver (Sohbet & Banka)", "balance {p} && tellraw {p} [{\"text\":\"[BANKA]: \",\"color\":\"gold\",\"bold\":true},{\"text\":\"Mevcut Akçe Bakiyeniz: \",\"color\":\"yellow\"},{\"score\":{\"name\":\"{p}\",\"objective\":\"akce\"},\"color\":\"green\",\"bold\":true},{\"text\":\" 🪙 Akçe\",\"color\":\"gold\"}]", "Oyuncunun sohbetine hem Vault hem skor tablosu bakiyesini gönderir"),

        ("🪙 64x Fiziksel Bakır Akçe Ver", 'minecraft:give {p} iron_nugget{display:{Name:\'{"text":"🪙 1x Bakır Akçe","color":"yellow","bold":true}\',Lore:[\'{"text":"Temel harcama akçesi","color":"gray"}\']}} {qty}', "El ile tutulup takas yapılabilen bakır para"),
        ("💰 64x Fiziksel Gümüş Akçe Ver", 'minecraft:give {p} gold_nugget{display:{Name:\'{"text":"💰 10x Gümüş Akçe","color":"gold","bold":true}\',Lore:[\'{"text":"Tüccar gümüş akçesi","color":"gray"}\']}} {qty}', "10 Akçe değerinde gümüş sikke"),
        ("👑 64x Fiziksel Altın Akçe Ver", 'minecraft:give {p} gold_ingot{display:{Name:\'{"text":"👑 100x Altın Akçe","color":"yellow","bold":true}\',Lore:[\'{"text":"Değerli altın külçe akçe","color":"gray"}\']}} {qty}', "100 Akçe değerinde saf altın külçe"),
        ("💎 64x Zümrüt Kraliyet Akçesi", 'minecraft:give {p} emerald{display:{Name:\'{"text":"💎 1.000x Zümrüt Kraliyet Akçesi","color":"green","bold":true}\',Lore:[\'{"text":"Kraliyet zümrüt serveti","color":"gray"}\']}} {qty}', "1.000 Akçe değerinde zümrüt mücevher"),
        ("🌌 64x Elmas Milyarder Akçesi", 'minecraft:give {p} diamond{display:{Name:\'{"text":"🌌 10.000x Elmas Milyarder Akçesi","color":"aqua","bold":true}\',Lore:[\'{"text":"Milyarder elmas akçesi","color":"gray"}\']}} {qty}', "100.000 Akçe değerinde elmas birim"),
        ("🧱 64x Netherite İmparatorluk Külçesi", 'minecraft:give {p} netherite_ingot{display:{Name:\'{"text":"🧱 100.000x Netherite İmparatorluk Külçesi","color":"dark_purple","bold":true}\',Lore:[\'{"text":"Devasa imparatorluk serveti","color":"gray"}\']}} {qty}', "100.000 Akçe değerinde efsanevi külçe")
    ],

    # -------------------------------------------------------------------------
    # 4. MARKET & ÖZEL NPC TÜCCARLAR
    # -------------------------------------------------------------------------
    "🏪 MARKET & ÖZEL TÜCCARLAR": [
        ("🏛️ Büyük Ticaret Çarşısı İnşa Et",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 polished_deepslate && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 yellow_wool && execute at {p} run fill ~-4 ~3 ~-4 ~4 ~3 ~4 red_wool && execute at {p} run fill ~-5 ~ ~-5 ~-5 ~2 ~-5 spruce_fence && execute at {p} run fill ~5 ~ ~-5 ~5 ~2 ~-5 spruce_fence && execute at {p} run fill ~-5 ~ ~5 ~-5 ~2 ~5 spruce_fence && execute at {p} run fill ~5 ~ ~5 ~5 ~2 ~5 spruce_fence && execute at {p} run fill ~-3 ~ ~-3 ~3 ~ ~-3 barrel && execute at {p} run setblock ~-2 ~1 ~-3 lantern && execute at {p} run setblock ~2 ~1 ~-3 lantern && playsound minecraft:block.anvil.use master {p} ~ ~ ~ 1 1",
         "11x11 kapalı tente çatılı, varil tezgahlı ve fenerli devasa pazar yeri çarşısı inşa eder"),

        ("⚔️ Silah & Zırh Ustası Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"weaponsmith",level:5,type:"plains"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"⚔️ Silah & Zırh Ustası","color":"gold","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:10b},sell:{id:"netherite_sword",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"sharpness",lvl:5s},{id:"fire_aspect",lvl:2s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:15b},sell:{id:"netherite_pickaxe",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:5s},{id:"fortune",lvl:3s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:20b},sell:{id:"netherite_chestplate",Count:1b,tag:{Unbreakable:1b,Enchantments:[{id:"protection",lvl:4s},{id:"unbreaking",lvl:3s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:5b},sell:{id:"totem_of_undying",Count:2b},maxUses:9999999}]}}',
         "Altın Akçe ile Netherite silah, zırh ve ölümsüzlük totemi satan ölümsüz sabit tüccar"),

        ("🏗️ Mimar & Lüks Blokçu Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"mason",level:5,type:"plains"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"🏗️ Mimar & Lüks Blokçu","color":"aqua","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:1b},sell:{id:"smooth_quartz",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:1b},sell:{id:"deepslate_bricks",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:2b},sell:{id:"sea_lantern",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:2b},sell:{id:"tinted_glass",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:3b},sell:{id:"ochre_froglight",Count:64b},maxUses:9999999}]}}',
         "Kuvars, derin kayrak, fener ve özel mimari blokları istif halinde satan tüccar"),

        ("🪄 Baş Büyücü & Simyacı Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"cleric",level:5,type:"plains"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"🪄 Baş Büyücü & Simyacı","color":"light_purple","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:5b},sell:{id:"enchanted_book",Count:1b,tag:{StoredEnchantments:[{id:"mending",lvl:1s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:5b},sell:{id:"enchanted_book",Count:1b,tag:{StoredEnchantments:[{id:"sharpness",lvl:5s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:5b},sell:{id:"enchanted_book",Count:1b,tag:{StoredEnchantments:[{id:"fortune",lvl:3s}]}},maxUses:9999999},{buy:{id:"gold_ingot",Count:4b},sell:{id:"enchanted_book",Count:1b,tag:{StoredEnchantments:[{id:"silk_touch",lvl:1s}]}},maxUses:9999999}]}}',
         "Tamir (Mending), Keskinlik V, Servet III ve İpeksi Dokunuş kitapları satan bilge büyücü"),

        ("🌾 Çiftçi & Gurme Aşçı Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"farmer",level:5,type:"plains"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"🌾 Çiftçi & Gurme Aşçı","color":"green","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:1b},sell:{id:"golden_carrot",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:3b},sell:{id:"enchanted_golden_apple",Count:8b},maxUses:9999999},{buy:{id:"gold_ingot",Count:1b},sell:{id:"cooked_beef",Count:64b},maxUses:9999999}]}}',
         "Altın havuç, Notch elması ve pişmiş et satan usta çiftçi"),

        ("⚙️ Kızıltaş Mühendisi Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"armorer",level:5,type:"plains"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"⚙️ Kızıltaş Mühendisi","color":"red","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:2b},sell:{id:"tnt",Count:64b},maxUses:9999999},{buy:{id:"gold_ingot",Count:1b},sell:{id:"slime_block",Count:32b},maxUses:9999999},{buy:{id:"gold_ingot",Count:1b},sell:{id:"sticky_piston",Count:32b},maxUses:9999999},{buy:{id:"gold_ingot",Count:1b},sell:{id:"observer",Count:32b},maxUses:9999999}]}}',
         "TNT, balçık, yapışkan piston ve gözlemci satan sanayi mühendisi"),

        ("🕵️‍♂️ Gizli Karaborsacı Çağır",
         'execute at {p} run summon villager ~ ~ ~ {VillagerData:{profession:"nitwit",level:5,type:"swamp"},NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,CustomName:\'{"text":"🕵️‍♂️ Gizli Karaborsacı","color":"dark_red","bold":true}\',CustomNameVisible:1b,Offers:{Recipes:[{buy:{id:"gold_ingot",Count:10b},sell:{id:"barrier",Count:16b},maxUses:9999999},{buy:{id:"gold_ingot",Count:20b},sell:{id:"spawner",Count:1b},maxUses:9999999},{buy:{id:"gold_ingot",Count:15b},sell:{id:"light",Count:64b,tag:{BlockStateTag:{level:"15"}}},maxUses:9999999},{buy:{id:"gold_ingot",Count:25b},sell:{id:"elytra",Count:1b,tag:{Unbreakable:1b}},maxUses:9999999}]}}',
         "Bariyer, Spawner, Işık Bloğu ve Kırılmaz Elytra satan kaçakçı"),

        ("🧹 Çevredeki Tüccarları Temizle", "minecraft:kill @e[type=villager,distance=..15]", "15 blok içindeki çağrılan tüccarları temizler")
    ],

    # -------------------------------------------------------------------------
    # 5. EFSANEVİ SETLER & 32K SİLAHLAR
    # -------------------------------------------------------------------------
    "⚡ EFSANEVİ SETLER & 32K SİLAHLAR": [
        ("📦 FULL EFSANEVİ MASTER KİTİ (3 Sandık)", CMD_COMBO_FULL, "Zırh Sandığı + Silah Sandığı + İkmal Sandığı (Tek Tıkla Envantere)"),
        ("🛡️ Efsanevi Zırh Sandığı (Lvl 255)", CMD_BOX_ARMOR, "Netherite Kask, Göğüslük, Pantolon, Çizme, Elytra, Kalkan"),
        ("⚡ Efsanevi Silah & Alet Sandığı", CMD_BOX_WEAPONS, "Kılıç, Kazmalar, Balta, Kürek, Çapa, Yay, Arbalet, Mızrak"),
        ("💎 Efsanevi İkmal & Totem Sandığı", CMD_BOX_SUPPLIES, "128x Totem, 128x Notch Elma, Fişek, Kristal, Elmas Bloklar"),

        ("🗡️ Kıyamet Kılıcı (Tek Atan)",
         'minecraft:give {p} netherite_sword{Unbreakable:1b,Enchantments:[{id:"sharpness",lvl:255s},{id:"looting",lvl:255s},{id:"fire_aspect",lvl:255s},{id:"sweeping",lvl:255s},{id:"knockback",lvl:10s}]} 1',
         "Milyon hasar vuran, vurduğunu yakan ve yağmalayan efsanevi kılıç"),

        ("⛏️ Deprem Kazması (Lvl 255 Servet)",
         'minecraft:give {p} netherite_pickaxe{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"fortune",lvl:255s}]} 1',
         "Blokları anında eritir ve 1 elmastan yüzlerce elmas düşürür"),

        ("💎 İpeksi Efsane Kazma",
         'minecraft:give {p} netherite_pickaxe{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"silk_touch",lvl:1s}]} 1',
         "Blokları olduğu gibi kıran kırılmaz süper kazma"),

        ("🪓 Orman Baltası (Giga Hız)",
         'minecraft:give {p} netherite_axe{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"sharpness",lvl:255s},{id:"fortune",lvl:255s}]} 1',
         "Ağaçları tek vuruşta devirir ve dev hasar verir"),

        ("🥄 Sismik Kürek",
         'minecraft:give {p} netherite_shovel{Unbreakable:1b,Enchantments:[{id:"efficiency",lvl:255s},{id:"fortune",lvl:255s}]} 1',
         "Toprak ve kumu 0.001 saniyede silip süpürür"),

        ("🏹 Nükleer Sonsuzluk Yayı",
         'minecraft:give {p} bow{Unbreakable:1b,Enchantments:[{id:"power",lvl:255s},{id:"flame",lvl:255s},{id:"punch",lvl:50s},{id:"infinity",lvl:1s}]} 1',
         "1 okla sonsuz nükleer alevli ok atar, hedefleri haritadan siler"),

        ("🎯 Makineli Hızlı Arbalet",
         'minecraft:give {p} crossbow{Unbreakable:1b,Enchantments:[{id:"quick_charge",lvl:5s},{id:"multishot",lvl:1s},{id:"piercing",lvl:255s}]} 1',
         "Anında gerilir, 3 lü delen mermi gibi ok saçar"),

        ("🔱 Zeus Fırtına Mızrağı",
         'minecraft:give {p} trident{Unbreakable:1b,Enchantments:[{id:"impaling",lvl:255s},{id:"loyalty",lvl:3s},{id:"channeling",lvl:1s}]} 1',
         "Geri dönen yıldırımlı efsanevi mızrak"),

        ("👑 Efsanevi Miğfer (Lvl 255)", 'minecraft:give {p} netherite_helmet{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"respiration",lvl:255s},{id:"thorns",lvl:255s}]} 1', "Ölümsüz kask"),
        ("🛡️ Efsanevi Göğüslük (Lvl 255)", 'minecraft:give {p} netherite_chestplate{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"blast_protection",lvl:255s},{id:"thorns",lvl:255s}]} 1', "Patlama geçirmez göğüslük"),
        ("🛡️ Efsanevi Pantolon (Lvl 255)", 'minecraft:give {p} netherite_leggings{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"fire_protection",lvl:255s},{id:"thorns",lvl:255s}]} 1', "Yanmaz pantolon"),
        ("👟 Efsanevi Çizmeler (Lvl 255)", 'minecraft:give {p} netherite_boots{Unbreakable:1b,Enchantments:[{id:"protection",lvl:255s},{id:"unbreaking",lvl:255s},{id:"feather_falling",lvl:255s},{id:"thorns",lvl:255s}]} 1', "Düşüş hasarı sıfır bot"),
        ("🪽 Sonsuz Master Elytra", 'minecraft:give {p} elytra{Unbreakable:1b,Enchantments:[{id:"unbreaking",lvl:255s},{id:"mending",lvl:1s}]} 1', "Asla yıpranmayan sonsuz kanat"),
        ("🛡️ Aşılmaz Master Kalkan", 'minecraft:give {p} shield{Unbreakable:1b,Enchantments:[{id:"unbreaking",lvl:255s},{id:"thorns",lvl:255s}]} 1', "Vuranı geri püskürten kalkan")
    ],

    # -------------------------------------------------------------------------
    # 6. BÜYÜ & EFEKT LABORATUVARI
    # -------------------------------------------------------------------------
    "🪄 BÜYÜ & EFEKT LABORATUVARI": [
        ("👑 MEGA ULTRA BUFF (Tüm Bufflar)",
         "effect give {p} resistance 99999 5 true && effect give {p} strength 99999 100 true && effect give {p} speed 99999 3 true && effect give {p} haste 99999 255 true && effect give {p} night_vision 99999 0 true && effect give {p} saturation 99999 255 true && effect give {p} fire_resistance 99999 0 true && effect give {p} absorption 99999 10 true && playsound minecraft:item.totem.use master {p}",
         "Tam ölümsüzlük, tek atma, süper koşu, ışık hızında kırma ve sonsuz tokluk"),

        ("⛏️ Çılgın Madenci Hızı (Haste 255)", "effect give {p} haste 99999 255 true", "Bloklara dokunduğun mikrosaniyede parçalar"),
        ("🛡️ Hasarsızlık (Resistance V)", "effect give {p} resistance 99999 5 true", "Darbe, patlama ve lavdan sıfır hasar alır"),
        ("💪 Titan Gücü (Strength 100)", "effect give {p} strength 99999 100 true", "Yumrukla dahi Ender Dragon'a tek atar"),
        ("🏃 Flaş Koşu Hızı (Speed 5)", "effect give {p} speed 99999 4 true", "Şimşek gibi yüksek koşu temposu"),
        ("👁️ Sonsuz Gece Görüşü (Night Vision)", "effect give {p} night_vision 99999 0 true", "Zifiri karanlığı gündüz yapar"),
        ("💖 Anında Can Yenilenmesi (Regen 255)", "effect give {p} regeneration 99999 255 true", "Can barı ışık hızında dolar"),
        ("🔥 Ateş Bağışıklığı (Fire Resistance)", "effect give {p} fire_resistance 99999 0 true", "Lav ve ateşte rahatça yüzme"),
        ("🌊 Sualtı Hâkimiyeti (Conduit Power)", "effect give {p} conduit_power 99999 0 true", "Suda sınırsız nefes, görüş ve kırma hızı"),
        ("🦘 Süper Zıplama (Jump Boost 5)", "effect give {p} jump_boost 99999 4 true", "10 blok yükseğe sıçrama"),
        ("👻 Tam Görünmezlik (Invisibility)", "effect give {p} invisibility 99999 0 true", "Moblar ve oyuncular göremez"),
        ("🪶 Yavaş Düşüş (Slow Falling)", "effect give {p} slow_falling 99999 0 true", "Tüy gibi süzülür, düşüş hasarı almaz"),
        ("🌟 Köyün Kahramanı (Hero of Village V)", "effect give {p} hero_of_the_village 99999 4 true", "Köylüler eşyaları bedavaya yakın verir"),
        ("🐬 Yunus Zarafeti (Dolphins Grace)", "effect give {p} dolphins_grace 99999 0 true", "Suda roket gibi yüzme hızı"),
        ("✨ Ekstra Can Barı (Absorption 10)", "effect give {p} absorption 99999 10 true", "40 ekstra altın kalp ekler"),
        ("🍖 Sonsuz Doygunluk (Saturation)", "effect give {p} saturation 99999 255 true", "Açlık barı asla düşmez"),
        ("🧹 TÜM EFEKTLERİ TEMİZLE", "effect clear {p}", "Tüm iksir ve büyü etkilerini anında sıfırlar"),

        ("🗡️ Eldeki Silaha: Keskinlik V", "enchant {p} sharpness 5", "Eldeki silaha Sharpness V basar"),
        ("🛡️ Eldeki Zırha: Koruma IV", "enchant {p} protection 4", "Eldeki zırha Protection IV basar"),
        ("⛏️ Eldeki Alete: Verimlilik V", "enchant {p} efficiency 5", "Eldeki alete Efficiency V basar"),
        ("💎 Eldeki Kazmaya: Servet III", "enchant {p} fortune 3", "Eldeki kazmaya Fortune III basar"),
        ("✨ Eldeki Kazmaya: İpeksi Dokunuş", "enchant {p} silk_touch 1", "Eldeki kazmaya Silk Touch basar"),
        ("🏹 Eldeki Yaya: Güç V (Power)", "enchant {p} power 5", "Eldeki yaya Power V basar"),
        ("♾️ Eldeki Yaya: Sonsuzluk (Infinity)", "enchant {p} infinity 1", "Eldeki yaya Infinity basar"),
        ("🔧 Eldeki Eşyaya: Tamir (Mending)", "enchant {p} mending 1", "Eldeki eşyaya Mending basar"),
        ("🔨 Eldeki Eşyaya: Kırılmazlık III", "enchant {p} unbreaking 3", "Eldeki eşyaya Unbreaking III basar")
    ],

    # -------------------------------------------------------------------------
    # 7. SUNUCU EVENTLERİ & BOSS
    # -------------------------------------------------------------------------
    "🎪 EVENT & ÖZEL ETKİNLİKLER": [
        ("☄️ Meteor Yağmuru Eventi Başlat",
         'execute at {p} run summon fireball ~ ~25 ~ {direction:[0.0,-1.0,0.0],ExplosionPower:4} && execute at {p} run summon tnt ~ ~20 ~ {Fuse:40} && title @a title {"text":"☄️ METEOR DÜŞÜYOR!","color":"red","bold":true} && title @a subtitle {"text":"Sığınaklara Kaçın!","color":"gold"} && playsound minecraft:entity.generic.explode master @a ~ ~ ~ 10 0.5',
         "Gökyüzünden patlayan meteor topları ve TNT indirir, dev sarsıntı yaratır"),

        ("💰 Altın & Akçe Yağmuru Eventi",
         'execute at {p} run summon item ~-1 ~5 ~ {Item:{id:"gold_ingot",Count:32b}} && execute at {p} run summon item ~1 ~5 ~ {Item:{id:"diamond",Count:16b}} && execute at {p} run summon item ~ ~6 ~1 {Item:{id:"emerald",Count:32b}} && title @a title {"text":"💰 ALTIN YAĞMURU!","color":"gold","bold":true} && title @a subtitle {"text":"Ganimetleri Toplayın!","color":"yellow"} && playsound minecraft:entity.player.levelup master @a',
         "Oyuncunun üzerine gökten külçeler, elmaslar ve zümrütler yağdırır"),

        ("🧟 Zombi Kıyameti Dalgası",
         'execute at {p} run summon zombie ~3 ~ ~ {HandItems:[{id:"iron_sword",Count:1b},{}],ArmorItems:[{},{},{id:"iron_chestplate",Count:1b},{id:"iron_helmet",Count:1b}]} && execute at {p} run summon zombie ~-3 ~ ~ {HandItems:[{id:"iron_sword",Count:1b},{}],ArmorItems:[{},{},{id:"iron_chestplate",Count:1b},{id:"iron_helmet",Count:1b}]} && execute at {p} run summon zombie ~ ~ ~3 {HandItems:[{id:"iron_sword",Count:1b},{}],ArmorItems:[{},{},{id:"iron_chestplate",Count:1b},{id:"iron_helmet",Count:1b}]} && title @a title {"text":"🧟 ZOMBİ KIYAMETİ!","color":"dark_red","bold":true}',
         "Oyuncuyu zırhlı ve kılıçlı zombi sürüsüyle kuşatır"),

        ("👹 Boss Savaşı: Warden Kralı",
         'execute at {p} run summon warden ~ ~ ~ {CustomName:\'{"text":"👹 KARANLIKLAR HÜKÜMDARI","color":"dark_purple","bold":true}\'} && title @a title {"text":"👹 BOSS DOĞDU!","color":"dark_purple","bold":true} && playsound minecraft:entity.warden.emerge master @a',
         "Özel isimli korkunç Warden bossu doğurur"),

        ("💀 Boss Savaşı: 3 Başlı Wither",
         'execute at {p} run summon wither ~ ~5 ~ {CustomName:\'{"text":"💀 KIYAMET WITHER\'I","color":"dark_red","bold":true}\'} && title @a title {"text":"💀 WITHER ÇAĞRILDI!","color":"dark_red","bold":true} && playsound minecraft:entity.wither.spawn master @a',
         "Gökyüzünde 3 başlı Wither bossu başlatır"),

        ("🎆 Görkemli Havai Fişek Festivali",
         'execute at {p} run summon firework_rocket ~ ~ ~ {LifeTime:20,FireworksItem:{Flight:2,Explosions:[{Type:1,Colors:[I;16711680,65280,255],FadeColors:[I;16776960]}]}} && execute at {p} run summon firework_rocket ~2 ~ ~ {LifeTime:25,FireworksItem:{Flight:2,Explosions:[{Type:2,Colors:[I;16776960,16711935],FadeColors:[I;65535]}]}} && execute at {p} run summon firework_rocket ~-2 ~ ~ {LifeTime:30,FireworksItem:{Flight:3,Explosions:[{Type:4,Colors:[I;65535,16711680],FadeColors:[I;16777215]}]}} && title @a actionbar {"text":"🎆 KUTLAMA VE ŞÖLEN BAŞLADI!","color":"gold","bold":true}',
         "Çok renkli patlayan roketlerle gökyüzü festivali yapar"),

        ("⚡ 15'li Şimşek Kasırgası",
         "execute at {p} run summon lightning_bolt ~2 ~ ~ && execute at {p} run summon lightning_bolt ~-2 ~ ~ && execute at {p} run summon lightning_bolt ~ ~ ~2 && execute at {p} run summon lightning_bolt ~ ~ ~-2 && execute at {p} run summon lightning_bolt ~3 ~ ~3 && execute at {p} run summon lightning_bolt ~-3 ~ ~-3",
         "Hedefin etrafını dev yıldırımlarla bombalar")
    ],

    # -------------------------------------------------------------------------
    # 8. TROLL & OYUNCU YÖNETİMİ
    # -------------------------------------------------------------------------
    "🤡 TROLL & OYUNCU YÖNETİMİ": [
        ("🚀 Uzaya Fırlat (Y: 500)", "tp {p} ~ 500 ~", "Oyuncuyu stratosfere ışınlar, serbest düşüşe bırakır"),
        ("🕳️ Yerin Dibine Göm (Y: -58)", "tp {p} ~ -58 ~", "Katman kayasının dibine hapseder"),
        ("🧊 Cam Kafese Hapset", "execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~1 glass outline", "Oyuncunun etrafına hava alamaz cam kafes örer"),
        ("⬛ Obsidyen Hücreye Kapat", "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~2 ~1 obsidian outline", "Kırılması imkansız obsidyen hücre"),
        ("🕸️ Örümcek Ağına Göm", "execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~1 cobweb replace air", "Hareket edemeyecek şekilde ağlara dolar"),
        ("🔨 Kafasına Örs Düşür", "execute at {p} run setblock ~ ~4 ~ anvil", "Doğrudan kafasına 4 blok yukarıdan örs bırakır"),
        ("🔥 Ayaklarının Altını Yak", "execute at {p} run setblock ~ ~ ~ fire", "Ayağını ateşe verir"),
        ("🌊 Kafasından Lav Boşalt", "execute at {p} run setblock ~ ~2 ~ lava", "Kafasından aşağı kızgın lav akıtır"),
        ("💧 Kafasından Su Dök", "execute at {p} run setblock ~ ~2 ~ water", "Kafasından su boşaltır"),
        ("🤢 Aşırı Bulantı (Nausea 255)", "effect give {p} nausea 30 255 true", "Ekranı fırıl fırıl döndürüp midesini bulandırır"),
        ("🕶️ Körlük & Zifiri Karanlık", "effect give {p} blindness 30 255 true && effect give {p} darkness 30 255 true", "1 santim önünü bile göremez"),
        ("🥶 Dondur / Felç Et (Slowness 255)", "effect give {p} slowness 30 255 true", "Adım dahi atamaz, kaskatı kesilir"),
        ("🎈 Sonsuz Havaya Yükselt (Levitation)", "effect give {p} levitation 15 5 true", "Balon gibi gökyüzüne uçurur"),
        ("🍖 Açlık Krizine Sok", "effect give {p} hunger 30 255 true", "Açlık barını 1 saniyede sıfıra indirir"),
        ("🔊 Creeper Tıslaması (Jumpscare)", "playsound minecraft:entity.creeper.primed master {p} ~ ~ ~ 10 1", "Arkasında creeper patlayacakmış gibi ses çalar"),
        ("👹 Warden Çığlığı (Jumpscare)", "playsound minecraft:entity.warden.emerge master {p} ~ ~ ~ 10 1", "Korkunç Warden çıkış çığlığı ile korkutur"),
        ("🐲 Ejderha Kükremesi", "playsound minecraft:entity.ender_dragon.growl master {p} ~ ~ ~ 10 1", "Kulağında dev ejderha kükremesi patlatır"),
        ("🎒 Envanterini Tamamen Boşalt", "clear {p}", "Tüm envanterini ve zırhlarını siler"),
        ("🧲 Baş Aşağı Çevir (Dinnerbone)", 'minecraft:give {p} name_tag{display:{Name:\'{"text":"Dinnerbone"}\'}} 1', "Dinnerbone isim etiketi verir")
    ],

    # -------------------------------------------------------------------------
    # 9. IŞINLANMA & WARP NOKTALARI
    # -------------------------------------------------------------------------
    "📍 IŞINLANMA & WARP NOKTALARI": [
        ("🌳 Overworld Spawn'a Işınla (0, 100, 0)", "execute in minecraft:overworld run tp {p} 0 100 0", "Dünya ana doğma noktasına gönderir"),
        ("🌋 Nether Boyutuna Gönder (0, 70, 0)", "execute in minecraft:the_nether run tp {p} 0 70 0", "Cehennem boyutuna güvenli kata ışınlar"),
        ("🔮 The End Boyutuna Gönder (0, 70, 0)", "execute in minecraft:the_end run tp {p} 0 70 0", "Ejderha dünyasına ışınlar"),
        ("👥 Herkesi Bana Çek (TP All)", "tp @a {p}", "Tüm online oyuncuları bu oyuncunun yanına çeker"),
        ("🛏️ Doğma Noktası Ayarla (Spawnpoint)", "spawnpoint {p}", "Oyuncunun yeniden doğma noktasını burası yapar"),
        ("💎 Derin Maden Katına İn (Y: -55)", "tp {p} ~ -55 ~", "Doğrudan elmas seviyesine ışınlar"),
        ("☁️ Gökyüzü Kulesine Çık (Y: 200)", "tp {p} ~ 200 ~", "Bulutların üzerine ışınlar"),
        ("🧭 0, 0 Merkezine Git", "tp {p} 0 ~ 0", "X=0, Z=0 dünya merkezine ışınlar"),
        ("📍 1000 Blok İleri Işınla", "tp {p} ~1000 ~ ~", "Doğuya 1000 blok keşfe gönderir")
    ],

    # -------------------------------------------------------------------------
    # 10. DÜNYA, HAVA & ANTİ-LAG
    # -------------------------------------------------------------------------
    "⚙️ DÜNYA, HAVA & ANTİ-LAG": [
        ("🧹 LAG TEMİZLİĞİ: Yerdeki Çöpleri Sil", "minecraft:kill @e[type=item]", "Yerde biriken tüm item çöplerini silip lagı önler"),
        ("🧹 LAG TEMİZLİĞİ: Canavarları Sil", "difficulty peaceful && difficulty normal", "Tüm zararlı yaratık ve canavarları anında temizler"),
        ("🏹 Yerdeki Okları Temizle", "minecraft:kill @e[type=arrow]", "Saplanan okları temizler"),
        ("⚡ Full Lag & Çöp Temizliği (Eşyalar + Oklar + Küreler)", "minecraft:kill @e[type=item] && minecraft:kill @e[type=arrow] && minecraft:kill @e[type=experience_orb]", "Tüm yerdeki çöpleri, okları ve küreleri tek seferde temizler"),

        ("☀️ Sabah Yap (Day)", "time set day", "Güneş doğar"),
        ("🕛 Öğle Yap (Noon)", "time set noon", "Tam tepede güneş"),
        ("🌇 Gün Batımı (Sunset)", "time set 12000", "Romantik akşam batımı"),
        ("🌙 Gece Yap (Night)", "time set night", "Gece başlar"),

        ("☀️ Güneşli Hava (Clear)", "weather clear", "Yağmuru keser"),
        ("🌧️ Yağmur Yağdır (Rain)", "weather rain", "Yağmur başlatır"),
        ("⛈️ Fırtına & Şimşek (Thunder)", "weather thunder", "Yıldırımlı fırtına"),

        ("🛡️ Eşyalar Düşmesin (KeepInv AÇ)", "gamerule keepInventory true", "Ölünce eşyalar envanterde kalır"),
        ("❌ Eşyalar Düşsün (KeepInv KAPAT)", "gamerule keepInventory false", "Ölünce eşyalar saçılır"),
        ("🚫 Creeper / Mob Hasarını Kapat", "gamerule mobGriefing false", "Creeper patlayınca bloklar kırılmaz"),
        ("💥 Mob Hasarını Aç", "gamerule mobGriefing true", "Creeper blokları patlatabilir"),
        ("🧯 Yangın Yayılmasını Kapat", "gamerule doFireTick false", "Ateş yayılmaz"),
        ("⏸️ Zaman Akışını Sabitle", "gamerule doDaylightCycle false", "Saat durur"),
        ("▶️ Zaman Akışını Başlat", "gamerule doDaylightCycle true", "Saat ilerler"),

        ("🕊️ Zorluk: Barışçıl", "difficulty peaceful", "Canavarlar doğmaz"),
        ("⚔️ Zorluk: Normal", "difficulty normal", "Standart zorluk"),
        ("💀 Zorluk: Zor (Hard)", "difficulty hard", "Maksimum canavar gücü"),
        ("💾 Dünyayı Şimdi Kaydet (Flush)", "save-all flush", "Tüm dünya bloklarını diske kalıcı yazar"),
        ("📢 Sunucuya Altın Başlık Bas", 'title @a title {"text":"ULTIMATE SERVER","color":"gold","bold":true}', "Ekrana dev altın yazı"),
        ("💬 Kurucu Duyurusu Geç", "say [KURUCU]: Sunucumuza Hos Geldiniz!", "Sohbete duyuru geçer")
    ],

    # -------------------------------------------------------------------------
    # 11. MOB & CANLI ÇAĞIRICI
    # -------------------------------------------------------------------------
    "🐉 MOB & CANLI ÇAĞIRICI": [
        ("🐲 Ender Ejderhası Çağır", "summon ender_dragon ~ ~5 ~", "Ender Dragon oluşturur"),
        ("💀 Wither Boss Çağır", "summon wither ~ ~2 ~", "3 Başlı Wither çağırır"),
        ("👹 Warden Çağır", "summon warden ~ ~ ~", "Karanlık derinlik bekçisi Warden"),
        ("🤖 Demir Golem Çağır", "summon iron_golem ~ ~ ~", "Korumacı Demir Golem"),
        ("🐎 Eyerli Evcil At Çağır", 'summon horse ~ ~ ~ {Tame:1b,SaddleItem:{id:"saddle",Count:1b}}', "Binmeye hazır evcil at"),
        ("🐕 Sadık Evcil Kurt", "summon wolf ~ ~ ~ {Tame:1b}", "Sadık kurt"),
        ("🐈 Evcil Kedi", "summon cat ~ ~ ~ {Tame:1b}", "Creeper kaçıran kedi"),
        ("🧨 Patlayan TNT Çağır", "summon tnt ~ ~ ~ {Fuse:40}", "2 saniye sonra patlar"),
        ("⚡ Yıldırım Çarptır", "summon lightning_bolt ~ ~ ~", "Yıldırım indirir"),
        ("🧟 Zombi Sürüsü (5x)", "summon zombie ~ ~ ~ && summon zombie ~ ~ ~ && summon zombie ~ ~ ~ && summon zombie ~ ~ ~ && summon zombie ~ ~ ~", "5 adet zombi basar"),
        ("💀 İskelet Sürüsü (5x)", "summon skeleton ~ ~ ~ && summon skeleton ~ ~ ~ && summon skeleton ~ ~ ~ && summon skeleton ~ ~ ~ && summon skeleton ~ ~ ~", "5 adet iskelet basar")
    ],

    # -------------------------------------------------------------------------
    # 12. YETKİ & MOD YÖNETİMİ
    # -------------------------------------------------------------------------
    "👑 YETKİ & OYUNCU MODLARI": [
        ("👑 OP Yetkisi Ver", "op {p}", "Oyuncuyu yönetici (OP) yapar"),
        ("🚫 OP Yetkisini Al", "deop {p}", "OP yetkisini kaldırır"),
        ("💖 Canı & Açlığı Fulle (Heal)", "effect give {p} instant_health 1 255 true && effect give {p} saturation 1 255 true", "Can ve açlık barını anında doldurur"),
        ("🏕️ Hayatta Kalma (Survival)", "gamemode survival {p}", "Survival moduna geçirir"),
        ("🎨 Yaratıcı Mod (Creative)", "gamemode creative {p}", "Creative moduna geçirir"),
        ("👻 İzleyici Modu (Spectator)", "gamemode spectator {p}", "Duvarlardan geçen hayalet modu"),
        ("🧭 Macera Modu (Adventure)", "gamemode adventure {p}", "Blok kıramaz macera modu"),
        ("🌟 +100 Level Deneyim (XP)", "xp add {p} 100 levels", "100 Seviye XP yükler"),
        ("✨ +1000 Puan Deneyim (XP)", "xp add {p} 1000 points", "1000 Deneyim puanı verir"),
        ("👢 Sunucudan At (Kick)", "kick {p} Sunucudan cikarildiniz", "Oyuncuyu oyundan atar"),
        ("⛔ Oyuncuyu Yasakla (Ban)", "ban {p} Sunucudan yasaklandiniz", "Sunucudan banlar"),
        ("🔓 Banı Aç (Pardon)", "pardon {p}", "Yasağını kaldırır"),
        ("☠️ Oyuncuyu Öldür", "kill {p}", "Anında öldürür")
    ],

    # -------------------------------------------------------------------------
    # 13. 🏡 ARSA & ARAZİ YÖNETİMİ (GriefPrevention)
    # -------------------------------------------------------------------------
    "🏡 ARSA & ARAZİ YÖNETİMİ": [
        ("⛏️ Arsa Kapatma Altın Küreği Ver", 'minecraft:give {p} golden_shovel{display:{Name:\'{"text":"🏡 Arsa Kapatma & Koruma Küreği","color":"gold","bold":true}\',Lore:[\'{"text":"İki çapraz köşeye sağ tıklayarak arsa kapat","color":"yellow"}\',\'{"text":"Sandıkların ve evlerin patlamaya karşı korunur!","color":"green"}\']}} 1', "Sağ tıklayarak sınırları çizip arsayı sahiplenme küreği"),
        ("📜 Oyuncunun Arsalarını Listele", "claimslist {p}", "Oyuncunun sahip olduğu tüm arsaları ve kalan blok hakkını listeler"),
        ("🛡️ +500 Bonus Arsa Bloğu Hediye Et", "adjustbonusclaimblocks {p} 500", "Oyuncuya 500 blokluk ekstra arsa genişletme hakkı verir"),
        ("🛡️ +2.000 Bonus Arsa Bloğu Hediye Et", "adjustbonusclaimblocks {p} 2000", "Oyuncuya 2.000 blokluk devasa arsa alanı verir"),
        ("🛡️ +10.000 Bonus Arsa Bloğu (Dev Şehir)", "adjustbonusclaimblocks {p} 10000", "Oyuncuya 10.000 blokluk krallık/şehir arsa hakkı verir"),
        ("💥 Arsa Patlama Korumasını Aç / Kapat", "sudo {p} claimexplosions", "Arsa içinde TNT/Creeper patlama hasarını açar veya kapatır"),
        ("🤝 Arsayı Arkadaşa Aç (Güven Ver - Trust)", "sudo {p} trust MIRKUNDAKLAYAN", "Seçilen oyuncuya arsa içinde inşa ve sandık izni verir"),
        ("🚫 Arsa Güvenini Kaldır (Untrust)", "sudo {p} untrust MIRKUNDAKLAYAN", "Arsa iznini geri alır"),
        ("📦 Sandık ve Eşya Güveni Ver (ContainerTrust)", "sudo {p} containertrust MIRKUNDAKLAYAN", "Yalnızca sandık ve fırınları açma izni verir"),
        ("🚪 Giriş & Buton Güveni Ver (AccessTrust)", "sudo {p} accesstrust MIRKUNDAKLAYAN", "Kapıları ve şalterleri kullanma izni verir"),
        ("🏰 Admin Koruma Alanı Oluştur (AdminClaim)", "sudo {p} adminclaims", "Sunucu doğma alanı veya pazar yeri için kırılmaz admin arsası"),
        ("🧹 Oyuncunun Tüm Arsalarını Sil", "deleteallclaims {p}", "Oyuncunun dünyadaki tüm arsalarını serbest bırakır"),
        ("📖 Arsa Kılavuz Kitabı Ver", "claimbook {p}", "Oyuncuya nasıl arsa kapatacağını anlatan renkli rehber kitap verir")
    ],

    # -------------------------------------------------------------------------
    # 14. 🛒 OYUN İÇİ MARKET & TAKAS (EconomyShopGUI & Trade)
    # -------------------------------------------------------------------------
    "🛒 OYUN İÇİ MARKET & TAKAS": [
        ("🛒 Oyuncuya Market Menüsünü Aç (/shop)", "sudo {p} shop", "Ekrana eşyalar alıp satabileceği renkli GUI marketi açar"),
        ("🏷️ Hızlı Eşya Satış Menüsünü Aç (/sellgui)", "sudo {p} sellgui", "Envanterdeki eşyaları sürükleyip anında Akçeye çevirir"),
        ("💰 Tüm Eşyaları Sat & Akçe Kazan (/sellall)", "sudo {p} sellall", "Envanterdeki satılabilir tüm maden ve tarım ürünlerini satar"),
        ("🧭 Sunucu & Market Pusulası Ver", 'minecraft:give {p} compass{display:{Name:\'{"text":"🧭 Sunucu & Market Menüsü","color":"gold","bold":true}\',Lore:[\'{"text":"Sağ tıkla veya /n yaz: Marketi aç!","color":"yellow"}\',\'{"text":"Akçenle eşya alıp satabilirsin!","color":"green"}\']}} 1', "Eline sağ tıklayınca market menüsünü açan özel pusula verir"),
        ("🤝 İki Oyuncu Arasında Takas Başlat", "sudo {p} trade MIRKUNDAKLAYAN", "Güvenli dolandırıcılıksız eşya ve Akçe takas penceresi açar"),
        ("🪙 +1.000 Akçe Gönder (/eco give)", "eco give {p} 1000 && scoreboard players add {p} akce 1000", "Hem Vault hem skor tablosuna 1.000 Akçe yükler"),
        ("🪙 +10.000 Akçe Gönder (/eco give)", "eco give {p} 10000 && scoreboard players add {p} akce 10000", "Hem Vault hem skor tablosuna 10.000 Akçe yükler"),
        ("🪙 +100.000 Milyarder Akçesi Yükle", "eco give {p} 100000 && scoreboard players add {p} akce 100000", "Hem Vault hem skor tablosuna 100.000 Akçe yükler"),
        ("💸 -500 Akçe Kes (/eco take)", "eco take {p} 500 && scoreboard players remove {p} akce 500", "Hem Vault hem skor tablosundan 500 Akçe keser"),
        ("🎯 Akçe Bakiyesini Sabitle (/eco set)", "eco set {p} 5000 && scoreboard players set {p} akce 5000", "Oyuncunun Akçesini her iki tarafta 5.000 olarak sabitler"),
        ("🏆 En Zenginler Sıralaması (/baltop)", "baltop", "Sunucunun en zengin oyuncularını listeler"),
        ("🔄 Market Fiyatlarını Yenile (/eshop reload)", "eshop reload", "EconomyShopGUI ayarlarını ve fiyat listesini yeniler")
    ],

    # -------------------------------------------------------------------------
    # 15. 🛡️ ANTICHEAT & GÜVENLİK (GrimAC & AntiXray)
    # -------------------------------------------------------------------------
    "🛡️ ANTICHEAT & GÜVENLİK": [
                ("🛡️ Anti-Xray Engine Mode 2 Obfuscation Durumu",
         "antixray status && tellraw @a[tag=admin] [{\"text\":\"[GÜVENLİK]: \",\"color\":\"aqua\",\"bold\":true},{\"text\":\"Anti-Xray Engine Mode 2 Aktif! Madenler sahte bloklarla gizleniyor.\",\"color\":\"green\"}]",
         "Anti-Xray sahte maden kalkanı durumunu kontrol eder"),

        ("💎 Şüpheliye Sahte Elmas Tuzağı Kur (Honeypot)",
         "execute at {p} run setblock ~ ~-1 ~-2 deepslate_diamond_ore && tellraw @a[tag=admin] [{\"text\":\"[Honeypot]: \",\"color\":\"gold\",\"bold\":true},{\"text\":\"{p} oyuncusunun 2 blok önüne izlenen tuzak elmas yerleştirildi!\",\"color\":\"yellow\"}]",
         "Şüpheli oyuncunun görüş alanına gizli bir elmas cevheri yerleştirir ve takibe alır"),

        ("📢 Anti-Xray & Hile Kalkanı Duyurusu",
         "broadcast &8[&c&lGÜVENLİK&8] &eSunucumuzda &c&lAnti-Xray Engine Mode 2 (Obfuscation) &eaktiftir! &bSaydam doku paketleri ve maden hileleri tamamen körleştirilmiştir.",
         "Tüm sunucuya Anti-Xray korumasının aktif olduğunu ve hilelerin çalışmayacağını duyurur"),
("🛡️ GrimAC Durumunu Kontrol Et", "grim reload", "Grim AntiCheat motorunu kontrol eder ve kuralları tazeler"),
        ("🔍 Canlı Hile İhlal Bildirimleri (/grim verbose)", "grim verbose", "Hile şüphelilerini konsolda ve sohbette anlık takip eder"),
        ("👁️ Anti-Xray Engelleyici Durumu", "say [GÜVENLİK]: Spigot Anti-Xray Aktif! Madenler gizleniyor.", "X-Ray maden hilelerinin engellendiğini onaylar"),
        ("🧊 Hile Şüphelisini Dondur & Kitle", "effect give {p} slowness 60 255 true && effect give {p} mining_fatigue 60 255 true && title {p} title {\"text\":\"⚠️ KONTROL EDİLİYORSUNUZ\",\"color\":\"red\",\"bold\":true}", "Şüpheli oyuncuyu 60 saniye kilitler, hareketini ve kazmasını durdurur"),
        ("🔥 Buzu Çöz / Serbest Bırak", "effect clear {p} slowness && effect clear {p} mining_fatigue", "Oyuncunun dondurmasını kaldırır"),
        ("🏃 Hileciden Tüm Eşyaları Al & Temizle", "clear {p}", "Envanterini tamamen siler"),
        ("⚡ Yere Çak (Uçan Hileciyi İndir)", "effect give {p} levitation 1 255 true", "Fly açan oyuncuyu anında yere çiviler")
    ],

    # -------------------------------------------------------------------------
    # 16. ⛺ EVLER & HIZLI IŞINLANMA (EssentialsX)
    # -------------------------------------------------------------------------
    "⛺ EVLER & HIZLI IŞINLANMA": [
        ("⛺ Oyuncunun Evine Işınlan (/home)", "sudo {p} home", "Oyuncuyu kaydettiği güvenli evine ışınlar"),
        ("📍 Burayı Ev Olarak Kaydet (/sethome)", "sudo {p} sethome", "Oyuncunun durduğu yeri /home noktası olarak kaydeder"),
        ("🏛️ Başlangıç Spawn Alanına Git (/spawn)", "sudo {p} spawn", "Oyuncuyu güvenli sunucu başlangıç merkezine ışınlar"),
        ("🔮 Işınlanma İsteği Gönder (/tpa)", "sudo {p} tpa MIRKUNDAKLAYAN", "Arkadaşına ışınlanma daveti yollar"),
        ("✅ Işınlanma İsteğini Kabul Et (/tpaccept)", "sudo {p} tpaccept", "Gelen ışınlanma davetini onaylar"),
        ("🏃 Önceki Konuma / Öldüğün Yere Dön (/back)", "sudo {p} back", "Ölüm veya önceki ışınlanma noktasına geri döner")
    ],

    # -------------------------------------------------------------------------
    # 17. 🎁 KİTLER & SUNUCU EKRANI (Kits, Scoreboard & Hologram)
    # -------------------------------------------------------------------------
    "🎁 KİTLER & EKRAN": [
        ("🎁 Oyuncuya Başlangıç Kiti Ver (/kit baslangic)", "kit baslangic {p}", "Taş aletler, altın arsa küreği, yiyecek, meşale ve 100 Akçe"),
        ("⭐ Oyuncuya Günlük Hediye Kiti Ver (/kit gunluk)", "kit gunluk {p}", "Altın elma, demir külçeler, ekmek, roket ve 500 Akçe ödülü"),
        ("⛏️ Oyuncuya Madenci Kiti Ver (/kit madenci)", "kit madenci {p}", "Verimlilik I demir kazma, 64 meşale, su kovası ve ekmek"),
        ("⚔️ Oyuncuya Savaşçı Kiti Ver (/kit savasci)", "kit savasci {p}", "Keskinlik I demir kılıç, kalkan, yay ve 32 ok"),
        ("📊 Scoreboard'u Aç/Kapat (/sb)", "sudo {p} sb", "Sağ taraftaki Akçe ve ping bilgi tablosunu açıp kapatır"),
        ("🌌 Spawn Rehber Hologramını Yenile (/dh reload)", "dh reload", "Spawn alanındaki rehber ve bilgi hologramını yeniler"),
        ("📢 Sohbette Market Duyurusu Geç", "broadcast &8[&6Duyuru&8] &e/n &7veya &e/shop &ayazarak Akçe marketini açabilirsiniz!", "Tüm sunucuya market duyurusu atar"),
        ("📢 Sohbette Arsa Duyurusu Geç", "broadcast &8[&6Duyuru&8] &eAltın Kürek &aile iki köşeye tıklayarak patlamaz arsanızı kapatın!", "Tüm sunucuya arsa duyurusu atar"),
        ("📢 Sohbette Takas Duyurusu Geç", "broadcast &8[&6Duyuru&8] &e/takas <oyuncu> &aile güvenli ticaret yapabilirsiniz!", "Tüm sunucuya takas duyurusu atar")
    ],

    # -------------------------------------------------------------------------
    # 18. 👑 ROLLER & MESLEK YÖNETİMİ
    # -------------------------------------------------------------------------
    "👑 ROLLER & MESLEKLER": [
        ("🏛️ Cumhurbaşkanı Rolü Ata", "team join cumhurbaskani {p} && tab player {p} tabprefix &c&l[Baskan] &e && tab player {p} tagprefix &c&l[Baskan] &e && title {p} title {\"text\":\"👑 CUMHURBAŞKANI SEÇİLDİNİZ!\",\"color\":\"red\",\"bold\":true} && broadcast &8[&4Devlet&8] &c{p} &4Cumhurbaskani makamina atandi!", "Oyuncuyu en yüksek devlet makamı olan Cumhurbaşkanı yapar"),
        ("🏡 Köy Muhtarı Rolü Ata", "team join muhtar {p} && tab player {p} tabprefix &6&l[Muhtar] &f && tab player {p} tagprefix &6&l[Muhtar] &f && title {p} title {\"text\":\"🏡 KÖY MUHTARI OLDUNUZ!\",\"color\":\"gold\",\"bold\":true} && broadcast &8[&6Duyuru&8] &e{p} &6Koy Muhtari secildi!", "Oyuncuyu köyün yöneticisi ve arsa temsilcisi Muhtar yapar"),
        ("👮 Polis Memuru Ata", "team join polis {p} && tab player {p} tabprefix &9&l[Polis] &b && tab player {p} tagprefix &9&l[Polis] &b && title {p} title {\"text\":\"👮 POLİS MEMURU OLDUNUZ!\",\"color\":\"blue\",\"bold\":true} && broadcast &8[&9Emniyet&8] &b{p} &9Polis Teskilatina katildi!", "Asayişi ve huzuru sağlamak için polis unvanı verir"),
        ("🪖 Asker & Komutan Ata", "team join asker {p} && tab player {p} tabprefix &2&l[Asker] &a && tab player {p} tagprefix &2&l[Asker] &a && title {p} title {\"text\":\"🪖 ASKER OLDUNUZ!\",\"color\":\"dark_green\",\"bold\":true} && broadcast &8[&2Ordu&8] &a{p} &2Milli Savunma Ordusuna katildi!", "Vatan savunması ve sınır güvenliği için asker unvanı verir"),
        ("🩺 Başhekim / Doktor Ata", "team join doktor {p} && tab player {p} tabprefix &c&l[Doktor] &f && tab player {p} tagprefix &c&l[Doktor] &f && title {p} title {\"text\":\"🩺 DOKTOR OLDUNUZ!\",\"color\":\"red\",\"bold\":true} && broadcast &8[&cSaglik&8] &f{p} &cDoktor gorevine basladi!", "Oyuncuları iyileştiren sağlık görevlisi unvanı verir"),
        ("⚖️ Ağır Ceza Hakimi Ata", "team join hakim {p} && tab player {p} tabprefix &5&l[Hakim] &d && tab player {p} tagprefix &5&l[Hakim] &d && title {p} title {\"text\":\"⚖️ HAKİM OLDUNUZ!\",\"color\":\"dark_purple\",\"bold\":true} && broadcast &8[&5Adalet&8] &d{p} &5Hakim olarak divana gecti!", "Oyuncular arası davaları çözen adalet hakimi yapar"),
        ("🏗️ Baş Mimar Ata", "team join mimar {p} && tab player {p} tabprefix &3&l[Mimar] &b && tab player {p} tagprefix &3&l[Mimar] &b && title {p} title {\"text\":\"🏗️ BAŞ MİMAR OLDUNUZ!\",\"color\":\"dark_aqua\",\"bold\":true} && broadcast &8[&3Imar&8] &b{p} &3Bas Mimar unvanini kazandi!", "Şehir yapılarını tasarlayan baş mimar yapar"),
        ("💰 Büyük Tüccar Ata", "team join tuccar {p} && tab player {p} tabprefix &e&l[Tuccar] &6 && tab player {p} tagprefix &e&l[Tuccar] &6 && title {p} title {\"text\":\"💰 BÜYÜK TÜCCAR OLDUNUZ!\",\"color\":\"yellow\",\"bold\":true} && broadcast &8[&eTicaret&8] &e{p} &6Buyuk Tuccar oldu!", "Pazarda ticaret yapan tüccar unvanı verir"),
        ("⛏️ Usta Madenci Ata", "team join madenci {p} && tab player {p} tabprefix &8&l[Madenci] &7 && tab player {p} tagprefix &8&l[Madenci] &7 && title {p} title {\"text\":\"⛏️ MADENCİ OLDUNUZ!\",\"color\":\"gray\",\"bold\":true}", "Yeraltı madenlerini işleten madenci unvanı verir"),
        ("🌾 Baş Çiftçi Ata", "team join ciftci {p} && tab player {p} tabprefix &a&l[Ciftci] &2 && tab player {p} tagprefix &a&l[Ciftci] &2 && title {p} title {\"text\":\"🌾 ÇİFTÇİ OLDUNUZ!\",\"color\":\"green\",\"bold\":true}", "Tarlaları ekip biçen çiftçi unvanı verir"),
        ("⚔️ Kraliyet Şövalyesi Ata", "team join sovalye {p} && tab player {p} tabprefix &1&l[Sovalye] &9 && tab player {p} tagprefix &1&l[Sovalye] &9 && title {p} title {\"text\":\"⚔️ KRALİYET ŞÖVALYESİ OLDUNUZ!\",\"color\":\"dark_blue\",\"bold\":true}", "Kralın özel muhafız şövalyesi yapar"),
        ("👑 Sunucu Kurucusu / Kral Yap", "team join kurucu {p} && tab player {p} tabprefix &4&l[Kurucu] &c && tab player {p} tagprefix &4&l[Kurucu] &c && title {p} title {\"text\":\"👑 SUNUCU KURUCUSU / KRAL!\",\"color\":\"dark_red\",\"bold\":true}", "En üst düzey Kurucu ve Hükümdar yetki unvanı verir"),
        ("❌ Rolü Sıfırla (Standart Vatandaş Yap)", "team join vatandas {p} && tab player {p} tabprefix &7[Vatandas] &f && tab player {p} tagprefix &7[Vatandas] &f && title {p} title {\"text\":\"Standart Vatandaş Yapıldınız\",\"color\":\"white\"}", "Özel rolü kaldırıp normal oyuncu/vatandaş seviyesine çeker")
    ],

    # -------------------------------------------------------------------------
    # 19. 🎰 CASİNO & ŞANS OYUNLARI (25+ Hazır Makine & Kumarhane)
    # -------------------------------------------------------------------------
    "🎰 CASİNO & ŞANS OYUNLARI": [
        ("🎰 Oyuncuya Canlı Casino Menüsünü Aç (/casino)",
         "sudo {p} casino",
         "Oyuncunun ekranına interaktif GUI Slot, Rulet, Crash ve Çarkıfelek menüsünü açar"),

        ("🎡 Canlı Büyük Şans Çarkını Aç (/casino wheel)",
         "sudo {p} casino wheel",
         "Oyuncuya animasyonlu dönen büyük Fortune Wheel şans çarkını açar"),

        ("🎁 Günlük Ücretsiz Şans Çarkını Aç (/casino daily)",
         "sudo {p} casino daily",
         "Her gün 1 kez ücretsiz çevrilebilen günlük ödül çarkını açar"),

        ("🏆 Casino En Çok Kazananlar Tablosu (/casino top)",
         "sudo {p} casino top",
         "Sunucuda casinodan en çok Akçe kazanan şanslı oyuncuların liderlik tablosunu açar"),

        ("💰 Kumarbaz Başlangıç Kredisi Ver (+5.000 Akçe)",
         "eco give {p} 5000 && scoreboard players add {p} akce 5000 && title {p} title {\"text\":\"🎰 CASİNOYA HOŞ GELDİNİZ!\",\"color\":\"gold\",\"bold\":true} && title {p} subtitle {\"text\":\"5.000 Akçe Kumar Kredisi Hesabınıza Yüklendi!\",\"color\":\"yellow\"} && playsound minecraft:entity.player.levelup master {p}",
         "Oyuncunun hem Vault hem skor tablosuna 5.000 Akçe casino kredisi tanımlar"),

        ("🕹️ ÇALIŞAN KOLLU & BUTONLU SLOT MAKİNESİ (İn-Game)",
         "execute at {p} run fill ~-1 ~-1 ~2 ~1 ~-1 ~2 polished_blackstone && execute at {p} run fill ~-1 ~ ~2 ~1 ~3 ~2 polished_blackstone && execute at {p} run fill ~-1 ~1 ~2 ~1 ~1 ~2 gold_block && execute at {p} run setblock ~ ~1 ~2 sea_lantern && execute at {p} run setblock ~ ~ ~1 dropper[facing=south]{Items:[{Slot:0b,id:\"diamond\",Count:16b},{Slot:1b,id:\"emerald\",Count:32b},{Slot:2b,id:\"gold_ingot\",Count:64b},{Slot:3b,id:\"gold_nugget\",Count:64b},{Slot:4b,id:\"netherite_ingot\",Count:4b},{Slot:5b,id:\"enchanted_golden_apple\",Count:4b},{Slot:6b,id:\"paper\",Count:10b,tag:{display:{Name:'{\"text\":\"💰 5.000 Akçe Çeki\",\"color\":\"gold\",\"bold\":true}'}}}]} && execute at {p} run setblock ~ ~1 ~1 stone_button[face=floor] && execute at {p} run setblock ~ ~-1 ~1 note_block && execute at {p} run setblock ~ ~2 ~1 oak_wall_sign[facing=north]{front_text:{messages:['{\"text\":\"🎰 KOLLU SLOT 🎰\",\"bold\":true,\"color\":\"gold\"}','{\"text\":\"Butona Bas!\",\"color\":\"yellow\"}','{\"text\":\"Elmas & Akçe\",\"color\":\"aqua\"}','{\"text\":\"Kazan!\",\"color\":\"green\"}']}} && playsound minecraft:block.anvil.use master {p} ~ ~ ~ 1 1",
         "Hedef oyuncunun önüne basıldığında zili çalan ve haznesinden elmas/akçe fırlatan fiziksel slot makinesi kurar"),

        ("🏰 Las Vegas Kumarhanesi & Casino Binası İnşa Et",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 polished_blackstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~4 ~6 air && execute at {p} run fill ~-6 ~ ~-6 ~6 ~3 ~6 red_concrete outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-6 ~4 ~-6 ~6 ~4 ~6 gold_block outline && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 sea_lantern && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 green_wool && execute at {p} run setblock ~ ~-1 ~ emerald_block && execute at {p} run setblock ~ ~ ~ jukebox && execute at {p} run setblock ~-3 ~ ~-3 chest && execute at {p} run setblock ~3 ~ ~-3 chest && execute at {p} run setblock ~ ~ ~-6 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-6 oak_door[half=upper,facing=north] && playsound minecraft:block.bell.use master {p} ~ ~ ~ 1 1",
         "13x13 kırmızı betonlu, altın çatılı, zümrüt masalı ve lüks zeminli kumarhane binası"),

        ("🎡 Dev Işıklı Rulet Masası & Bahis Alanı",
         "execute at {p} run fill ~-4 ~-1 ~-2 ~4 ~-1 ~2 polished_deepslate && execute at {p} run fill ~-3 ~ ~-1 ~3 ~ ~1 green_carpet && execute at {p} run fill ~-3 ~-1 ~-1 ~-1 ~-1 ~1 red_concrete && execute at {p} run fill ~1 ~-1 ~-1 ~3 ~-1 ~1 black_concrete && execute at {p} run setblock ~ ~-1 ~ emerald_block && execute at {p} run setblock ~ ~ ~ dropper[facing=up]{Items:[{Slot:0b,id:\"red_dye\",Count:16b,tag:{display:{Name:'{\"text\":\"🔴 Kırmızı 32\",\"color\":\"red\"}'}}},{Slot:1b,id:\"black_dye\",Count:16b,tag:{display:{Name:'{\"text\":\"⚫ Siyah 17\",\"color\":\"dark_gray\"}'}}},{Slot:2b,id:\"green_dye\",Count:2b,tag:{display:{Name:'{\"text\":\"🟢 Yeşil 0 (Mega Jackpot)\",\"color\":\"green\"}'}}}]} && execute at {p} run setblock ~ ~ ~1 stone_button[face=floor] && execute at {p} run setblock ~-4 ~ ~ sea_lantern && execute at {p} run setblock ~4 ~ ~ sea_lantern && playsound minecraft:block.bell.use master {p} ~ ~ ~ 1 1",
         "Kırmızı, siyah ve yeşil bölmeli, zümrüt kalpli, fırlatıcılı ve butonlu dev Rulet masası"),

        ("🃏 Lüks 21 (Blackjack) Oyun Masası & Dağıtıcı Koltuğu",
         "execute at {p} run fill ~-3 ~-1 ~-2 ~3 ~-1 ~2 dark_oak_planks && execute at {p} run fill ~-2 ~ ~-1 ~2 ~ ~1 green_wool && execute at {p} run setblock ~ ~ ~ lectern[facing=north] && execute at {p} run setblock ~ ~1 ~ sea_lantern && execute at {p} run setblock ~ ~ ~-1 dark_oak_stairs[facing=south] && execute at {p} run setblock ~-2 ~ ~1 dark_oak_stairs[facing=north] && execute at {p} run setblock ~ ~ ~1 dark_oak_stairs[facing=north] && execute at {p} run setblock ~2 ~ ~1 dark_oak_stairs[facing=north] && execute at {p} run setblock ~ ~-1 ~ chest && playsound minecraft:block.wood.place master {p} ~ ~ ~ 1 1",
         "Yeşil çuha kaplı, dağıtıcı koltuğu ve 3 oyuncu sandalyeli tam profesyonel 21 Blackjack masası"),

        ("🪙 Yazı-Tura & Coinflip Düello Standı",
         "execute at {p} run fill ~-2 ~-1 ~-1 ~2 ~-1 ~1 smooth_quartz && execute at {p} run setblock ~-1 ~ ~-1 red_carpet && execute at {p} run setblock ~1 ~ ~-1 blue_carpet && execute at {p} run setblock ~ ~ ~ redstone_lamp && execute at {p} run setblock ~ ~-1 ~ dropper[facing=up]{Items:[{Slot:0b,id:\"gold_nugget\",Count:32b,tag:{display:{Name:'{\"text\":\"🪙 TURA\",\"color\":\"gold\",\"bold\":true}'}}},{Slot:1b,id:\"iron_nugget\",Count:32b,tag:{display:{Name:'{\"text\":\"🪙 YAZI\",\"color\":\"white\",\"bold\":true}'}}}]} && execute at {p} run setblock ~ ~ ~1 stone_button[face=floor] && playsound minecraft:block.stone_button.click_on master {p} ~ ~ ~ 1 1",
         "Kırmızı ve Mavi taraflı, ortasında lamba ve rastgele yazı-tura fırlatıcısı olan düello standı"),

        ("🎲 Barbut & Çift Zar Masası (Dice Alley)",
         "execute at {p} run fill ~-3 ~-1 ~-2 ~3 ~-1 ~2 spruce_planks && execute at {p} run fill ~-3 ~ ~-2 ~3 ~ ~2 spruce_fence outline && execute at {p} run fill ~-2 ~ ~-1 ~2 ~ ~1 green_carpet && execute at {p} run setblock ~ ~ ~ dropper[facing=up]{Items:[{Slot:0b,id:\"white_dye\",Count:1b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 1\",\"color\":\"white\"}'}}},{Slot:1b,id:\"white_dye\",Count:2b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 2\",\"color\":\"white\"}'}}},{Slot:2b,id:\"white_dye\",Count:3b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 3\",\"color\":\"white\"}'}}},{Slot:3b,id:\"white_dye\",Count:4b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 4\",\"color\":\"white\"}'}}},{Slot:4b,id:\"white_dye\",Count:5b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 5\",\"color\":\"white\"}'}}},{Slot:5b,id:\"white_dye\",Count:6b,tag:{display:{Name:'{\"text\":\"🎲 ZAR: 6 (DÜŞEŞ)\",\"color\":\"gold\"}'}}}]} && execute at {p} run setblock ~ ~ ~-1 stone_button[face=floor] && playsound minecraft:block.wood.place master {p}",
         "Ahşap çit korumalı, yeşil zeminli ve 1-6 zar fırlatan mekanik barbut masası"),

        ("🕵️ Yeraltı Gizli Kumarhanesi (Gizli Kitaplık Girişli)",
         "execute at {p} run fill ~-5 ~-5 ~-5 ~5 ~-1 ~5 deepslate_tiles && execute at {p} run fill ~-4 ~-4 ~-4 ~4 ~-2 ~4 air && execute at {p} run fill ~-4 ~-5 ~-4 ~4 ~-5 ~4 red_carpet && execute at {p} run fill ~-5 ~-4 ~-5 ~-5 ~-2 ~5 bookshelf && execute at {p} run setblock ~ ~-2 ~ soul_lantern[hanging=true] && execute at {p} run setblock ~-3 ~-4 ~ barrel && execute at {p} run setblock ~3 ~-4 ~ barrel && execute at {p} run setblock ~ ~-4 ~-3 crafting_table && execute at {p} run setblock ~ ~-1 ~ iron_trapdoor && playsound minecraft:block.iron_trapdoor.open master {p} ~ ~ ~ 1 1",
         "Yerin altında gizli kitaplık duvarlı, varil masalı, kırmızı halılı gizli speakeasy kumarhanesi"),

        ("🎰 Canlı Slot Çevir (Jackpot: 💎 💎 💎 - 50.000 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎰 [ 💎 | 💎 | 💎 ]\",\"color\":\"aqua\",\"bold\":true} && title {p} subtitle {\"text\":\"🎉 MEGA JACKPOT! +50.000 Akçe Hesabınıza Eklendi!\",\"color\":\"gold\"} && eco give {p} 50000 && scoreboard players add {p} akce 50000 && playsound minecraft:ui.toast.challenge_complete master {p} ~ ~ ~ 1 1 && execute at {p} run summon firework_rocket ~ ~1 ~ {FireworksItem:{id:\"firework_rocket\",Count:1b,tag:{Fireworks:{Flight:2b,Explosions:[{Type:1,Colors:[I;16766720,65535]}]}}}} && broadcast &8[&6Casino&8] &e{p} &adünyanın en büyük &bMEGA JACKPOTUNU &avurdu! (+50.000 Akçe)",
         "3 adet elmas çarkını vuran oyuncuya dev havai fişek patlatır ve 50.000 Akçe verir"),

        ("🎰 Canlı Slot Çevir (Mega Kazanç: 7️⃣ 7️⃣ 7️⃣ - 20.000 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎰 [ 7️⃣ | 7️⃣ | 7️⃣ ]\",\"color\":\"gold\",\"bold\":true} && title {p} subtitle {\"text\":\"⭐ 3x YEDİ! +20.000 Akçe Kazandınız!\",\"color\":\"yellow\"} && eco give {p} 20000 && scoreboard players add {p} akce 20000 && playsound minecraft:entity.player.levelup master {p} ~ ~ ~ 1 1 && broadcast &8[&6Casino&8] &e{p} &67-7-7 Şanslı Serisini yakaladı! (+20.000 Akçe)",
         "3'lü 7'li serisiyle 20.000 Akçe kazandırır ve sunucuya duyurur"),

        ("🎰 Canlı Slot Çevir (Altın Çan: 🔔 🔔 🔔 - 10.000 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎰 [ 🔔 | 🔔 | 🔔 ]\",\"color\":\"yellow\",\"bold\":true} && title {p} subtitle {\"text\":\"🔔 ALTIN ÇANLAR! +10.000 Akçe Kazandınız!\",\"color\":\"gold\"} && eco give {p} 10000 && scoreboard players add {p} akce 10000 && playsound minecraft:block.bell.use master {p} ~ ~ ~ 1 1",
         "Üçlü altın çan sesi çalar ve 10.000 Akçe kazandırır"),

        ("🎰 Canlı Slot Çevir (Kiraz Bonusu: 🍒 🍒 🍒 - 5.000 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎰 [ 🍒 | 🍒 | 🍒 ]\",\"color\":\"red\",\"bold\":true} && title {p} subtitle {\"text\":\"🍒 ÜÇ KİRAZ! +5.000 Akçe Kazandınız!\",\"color\":\"light_purple\"} && eco give {p} 5000 && scoreboard players add {p} akce 5000 && playsound minecraft:entity.experience_orb.pickup master {p} ~ ~ ~ 1 1.5",
         "3 adet kiraz kazancı ile 5.000 Akçe verir"),

        ("🎰 Canlı Slot Çevir (Kaybettin: 🍋 🍒 🔔 - 0 Akçe)",
         "title {p} times 5 30 10 && title {p} title {\"text\":\"🎰 [ 🍋 | 🍒 | 🔔 ]\",\"color\":\"gray\",\"bold\":true} && title {p} subtitle {\"text\":\"❌ Kazanamadınız! Şansınızı tekrar deneyin.\",\"color\":\"red\"} && playsound minecraft:block.chest.locked master {p} ~ ~ ~ 1 0.7",
         "Gerçekçi slot kaybetme animasyonu ve sesi oynatır"),

        ("🎡 Canlı Rulet Oyna (Kırmızı 32 Kazandı! - 2.500 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎡 RULET ÇARKI DÖNÜYOR...\",\"color\":\"yellow\"} && title {p} subtitle {\"text\":\"Top Kırmızı 32'de durdu! 🔴\",\"color\":\"red\"} && tellraw {p} [{\"text\":\"🎡 [RULET]: \",\"color\":\"red\",\"bold\":true},{\"text\":\"Kırmızı 32 Kazandı! +2.500 Akçe hesabınıza yüklendi.\",\"color\":\"gold\"}] && eco give {p} 2500 && scoreboard players add {p} akce 2500 && playsound minecraft:block.note_block.chime master {p} ~ ~ ~ 1 1.2",
         "Rulette topun Kırmızı 32'ye gelmesini simüle eder ve 2.500 Akçe kazandırır"),

        ("🎡 Canlı Rulet Oyna (Siyah 17 Kazandı! - 2.500 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎡 RULET ÇARKI DÖNÜYOR...\",\"color\":\"yellow\"} && title {p} subtitle {\"text\":\"Top Siyah 17'de durdu! ⚫\",\"color\":\"dark_gray\"} && tellraw {p} [{\"text\":\"🎡 [RULET]: \",\"color\":\"dark_gray\",\"bold\":true},{\"text\":\"Siyah 17 Kazandı! +2.500 Akçe hesabınıza yüklendi.\",\"color\":\"gold\"}] && eco give {p} 2500 && scoreboard players add {p} akce 2500 && playsound minecraft:block.note_block.chime master {p} ~ ~ ~ 1 1.2",
         "Rulette topun Siyah 17'ye gelmesini simüle eder ve 2.500 Akçe kazandırır"),

        ("🎡 Canlı Rulet Oyna (Yeşil 0 MEGA VURGUN! - 50.000 Akçe)",
         "title {p} times 5 50 10 && title {p} title {\"text\":\"🟢 YEŞİL SIFIR! (0)\",\"color\":\"green\",\"bold\":true} && title {p} subtitle {\"text\":\"🎉 1/37 İMKANSIZ İHTİMAL! +50.000 Akçe Kazandınız!\",\"color\":\"gold\"} && eco give {p} 50000 && scoreboard players add {p} akce 50000 && playsound minecraft:ui.toast.challenge_complete master {p} ~ ~ ~ 1 1 && broadcast &8[&aRulet&8] &e{p} &bYeşil Sıfır (0) &avurgununu yaptı! (+50.000 Akçe)",
         "Ruletin en zor ve yüksek kazançlı Yeşil 0 sonucunu verir, sunucuya duyurur"),

        ("🪙 Canlı Yazı-Tura (TURA GELDİ! - +1.000 Akçe)",
         "title {p} times 5 30 10 && title {p} title {\"text\":\"🪙 TURA!\",\"color\":\"gold\",\"bold\":true} && title {p} subtitle {\"text\":\"Bahsi Kazandınız! +1.000 Akçe\",\"color\":\"green\"} && eco give {p} 1000 && scoreboard players add {p} akce 1000 && playsound minecraft:entity.experience_orb.pickup master {p} ~ ~ ~ 1 1.5",
         "Yazı-Tura atışında Tura getirir ve 1.000 Akçe kazandırır"),

        ("🪙 Canlı Yazı-Tura (YAZI GELDİ! - +1.000 Akçe)",
         "title {p} times 5 30 10 && title {p} title {\"text\":\"🪙 YAZI!\",\"color\":\"white\",\"bold\":true} && title {p} subtitle {\"text\":\"Bahsi Kazandınız! +1.000 Akçe\",\"color\":\"green\"} && eco give {p} 1000 && scoreboard players add {p} akce 1000 && playsound minecraft:entity.experience_orb.pickup master {p} ~ ~ ~ 1 1.5",
         "Yazı-Tura atışında Yazı getirir ve 1.000 Akçe kazandırır"),

        ("🎲 Canlı Çift Zar At (12 Düşeş Geldi! - +5.000 Akçe)",
         "title {p} times 5 40 10 && title {p} title {\"text\":\"🎲 [ 6 ⚅ | 6 ⚅ ] - DÜŞEŞ!\",\"color\":\"gold\",\"bold\":true} && title {p} subtitle {\"text\":\"🎯 ÇİFT ALTI! +5.000 Akçe Kazandınız!\",\"color\":\"yellow\"} && eco give {p} 5000 && scoreboard players add {p} akce 5000 && playsound minecraft:entity.player.levelup master {p} ~ ~ ~ 1 1",
         "Çift zar atışında 6-6 düşeş getirir ve 5.000 Akçe verir"),

        ("🎲 Canlı Tek Zar At (1-6 Şans & 1.000 Akçe)",
         "playsound minecraft:block.note_block.bell master {p} ~ ~ ~ 1 1.5 && tellraw {p} [{\"text\":\"🎲 [ZAR ATILDI]: \",\"color\":\"gold\",\"bold\":true},{\"text\":\"Zar masada durdu: \",\"color\":\"yellow\"},{\"text\":\"⚄ 5 Geldi!\",\"color\":\"green\",\"bold\":true},{\"text\":\" (+1.000 Akçe)\",\"color\":\"aqua\"}] && eco give {p} 1000 && scoreboard players add {p} akce 1000",
         "Tek zar atar, sonucu ekranda bildirir ve 1.000 Akçe verir"),

        ("🎟️ Sunucu Geneli Büyük Piyango & Loto Çekilişi",
         "broadcast &e&l======================================== && broadcast &6&l🎟️ BÜYÜK SUNUCU PİYANGOSU ÇEKİLİYOR... && broadcast &aŞanslı numara belirlendi! Kazanan bilet sahibi: &e&l{p}! && broadcast &6Ödül: &e100.000 Akçe &6ve &bKraliyet Zümrütleri! && broadcast &e&l======================================== && title @a title {\"text\":\"🎟️ PİYANGO KAZANANI: {p}!\",\"color\":\"gold\",\"bold\":true} && eco give {p} 100000 && scoreboard players add {p} akce 100000 && playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 1",
         "Tüm sunucuya büyük loto çekilişi anonsu yapar ve hedefe 100.000 Akçe verir"),

        ("🎁 Efsanevi Jackpot Şans Kasası Ver",
         'minecraft:give {p} purple_shulker_box{display:{Name:\'{\"text\":\"🎰 GİZEMLİ JACKPOT ŞANS KASASI\",\"color\":\"gold\",\"bold\":true}\',Lore:[\'{\"text\":\"İçinde 100x Elmas, Zümrüt ve Kraliyet Akçeleri var!\",\"color\":\"yellow\"}\',\'{\"text\":\"Aç ve şansını dene!\",\"color\":\"green\"}\']},BlockEntityTag:{Items:[{Slot:0b,id:"diamond",Count:64b},{Slot:1b,id:"emerald",Count:64b},{Slot:2b,id:"gold_ingot",Count:64b},{Slot:3b,id:"netherite_ingot",Count:16b},{Slot:4b,id:"enchanted_golden_apple",Count:16b},{Slot:5b,id:"totem_of_undying",Count:8b}]}} 1',
         "Açıldığında içinden yüzlerce elmas, zümrüt, totem ve külçe fışkıran gizemli zenginlik kasası"),

        ("💣 Patlayan Şakacı Kumar Kasası (Troll)",
         "execute at {p} run summon tnt ~ ~ ~ && playsound minecraft:entity.creeper.primed master {p} ~ ~ ~ 1 1 && title {p} title {\"text\":\"💣 KASA PATLADI!\",\"color\":\"red\",\"bold\":true} && tellraw {p} [{\"text\":\"[CASİNO GÜVENLİK]: \",\"color\":\"red\",\"bold\":true},{\"text\":\"Hileli kasa tespit edildi, bomba patlatıldı!\",\"color\":\"yellow\"}]",
         "Şakacı tuzaklı kumar kasası, oyuncunun önünde patlayan zararsız TNT şovu yapar"),

        ("🏦 Casino Kasa Dairesi & Güvenlik Bankamatiği (ATM)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 iron_block && execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~1 reinforced_deepslate outline && execute at {p} run setblock ~ ~ ~-1 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-1 iron_door[half=upper,facing=north] && execute at {p} run setblock ~ ~ ~ dispenser[facing=north]{Items:[{Slot:0b,id:\"gold_ingot\",Count:64b},{Slot:1b,id:\"emerald\",Count:64b}]} && execute at {p} run setblock ~1 ~ ~-2 stone_button[face=wall,facing=north] && playsound minecraft:block.anvil.place master {p}",
         "Zırhlı derin kayrak ve demir bloklardan ATM para çekme ve kasa dairesi makinesi"),

        ("👑 VIP Kumarbaz Rütbesi & Parıltılı Başlık",
         "execute at {p} run scoreboard players tag {p} add vip_kumarbaz && execute at {p} run team add kumarbaz \"VIP Kumarbaz\" && execute at {p} run team modify kumarbaz prefix {\"text\":\"[VIP Kumarbaz] \",\"color\":\"gold\",\"bold\":true} && execute at {p} run team join kumarbaz {p} && effect give {p} glowing 99999 1 true && effect give {p} luck 99999 5 true && title {p} title {\"text\":\"👑 VIP KUMARBAZ OLDUNUZ!\",\"color\":\"gold\",\"bold\":true}",
         "Oyuncuya VIP Kumarbaz ünvanı, parlama ve seviye 5 Şans iksiri efekti tanımlar"),

        ("🎆 Devasa Casino Kutlama & Renkli Havai Fişek Şovu",
         "execute at {p} run summon firework_rocket ~ ~1 ~ {FireworksItem:{id:\"firework_rocket\",Count:1b,tag:{Fireworks:{Flight:1b,Explosions:[{Type:1,Colors:[I;16711680,65280,255]}]}}}} && execute at {p} run summon firework_rocket ~2 ~1 ~ {FireworksItem:{id:\"firework_rocket\",Count:1b,tag:{Fireworks:{Flight:2b,Explosions:[{Type:2,Colors:[I;16766720]}]}}}} && broadcast &8[&6Casino&8] &e{p} &aCasino Jackpotunu vurdu! 🎉 Tebrikler!",
         "Tüm sunucuya renkli havai fişeklerle kutlama duyurusu geçer")
    ],

    # -------------------------------------------------------------------------
    # 20. 🗳️ SEÇİM & DEMOKRASİ SİSTEMİ
    # -------------------------------------------------------------------------
    "🗳️ SEÇİM & DEMOKRASİ": [
        ("👑 Cumhurbaşkanlığı Seçimlerini Başlat",
         "broadcast &e&l======================================== && broadcast &6&l👑 RESMİ CUMHURBAŞKANLIĞI SEÇİMLERİ BAŞLADI! && broadcast &eOyunuzu vermek için sandığa gidiniz veya &a/oy <aday> &eyazınız! && broadcast &e&l======================================== && title @a title {\"text\":\"👑 CUMHURBAŞKANLIĞI SEÇİMİ!\",\"color\":\"gold\",\"bold\":true} && title @a subtitle {\"text\":\"Vatandaşlar sandık başına!\",\"color\":\"yellow\"} && playsound minecraft:ui.toast.challenge_complete master @a",
         "Tüm sunucuda Cumhurbaşkanlığı seçim sürecini başlatır, duyuru geçer ve oyuncuları oy vermeye davet eder"),

        ("🏡 Köy Muhtarlığı Seçimlerini Başlat",
         "broadcast &e&l======================================== && broadcast &6&l🏡 RESMİ KÖY MUHTARLIĞI SEÇİMLERİ BAŞLADI! && broadcast &eKöyünüzün yeni Muhtarını seçmek için &a/oy <aday> &eyazınız! && broadcast &e&l======================================== && title @a title {\"text\":\"🏡 MUHTARLIK SEÇİMİ!\",\"color\":\"green\",\"bold\":true} && title @a subtitle {\"text\":\"Köyün yeni Muhtarını seçin!\",\"color\":\"yellow\"} && playsound minecraft:entity.player.levelup master @a",
         "Köy Muhtarlığı seçimlerini başlatır, /oy komutunu hatırlatır"),

        ("🗳️ Seçim Sandığı & Oy Kabini İnşa Et",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 smooth_stone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 air && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 dark_oak_planks outline && execute at {p} run fill ~-1 ~ ~-2 ~1 ~1 ~-2 air && execute at {p} run setblock ~ ~ ~ barrel && execute at {p} run setblock ~ ~1 ~ oak_wall_sign[facing=south]{front_text:{messages:['{\"text\":\"🗳️ SEÇİM SANDIĞI\",\"bold\":true,\"color\":\"dark_blue\"}','{\"text\":\"Oyları buraya\",\"color\":\"black\"}','{\"text\":\"bırakınız.\",\"color\":\"black\"}','{\"text\":\"Gizli Oy Açık Tasnif\",\"color\":\"dark_red\"}']}} && execute at {p} run setblock ~-1 ~1 ~ torch && execute at {p} run setblock ~1 ~1 ~ torch && playsound minecraft:block.wood.place master {p}",
         "Oyuncunun bulunduğu yere resmi mühürlü Seçim Sandığı (fıçı) ve ahşap Oy Kabini inşa eder"),

        ("📜 Resmi Oy Pusulası & Mühür Dağıt",
         "minecraft:give {p} paper{display:{Name:'{\"text\":\"🗳️ Resmi Seçim Oy Pusulası\",\"color\":\"gold\",\"bold\":true}',Lore:['{\"text\":\"Adayınızın adını üzerine yazıp\",\"color\":\"yellow\"}','{\"text\":\"Seçim Sandığına bırakın veya /oy kullanın.\",\"color\":\"gray\"}']}} 1 && minecraft:give {p} feather{display:{Name:'{\"text\":\"✅ EVET / TERCİH MÜHRÜ\",\"color\":\"green\",\"bold\":true}',Lore:['{\"text\":\"Demokrasinin kutsal mührü.\",\"color\":\"yellow\"}']}} 1",
         "Hedef oyuncuya imzalı seçim pusulası ve EVET mührü verir"),

        ("☀️ Gündüz Olsun mu? Oylaması Başlat",
         "broadcast &8[&eOylama&8] &6Gündüz yapılsın mı? &aEvet için zıplayın, Hayır için eğilin! && playsound minecraft:block.note_block.bell master @a",
         "Halk oylaması ile havanın gündüz yapılması için oylama başlatır"),

        ("🌧️ Güneşli Hava (Yağmur Dursun) Oylaması",
         "broadcast &8[&bOylama&8] &bYağmur dursun mu? &a/weather clear &eyapılsın mı? && playsound minecraft:block.note_block.bell master @a",
         "Yağmurun dindirilmesi için sunucu genelinde oylama başlatır"),

        ("🏆 Seçim Sonucu: {p} Cumhurbaşkanı Seçildi!",
         "team join cumhurbaskani {p} && tab player {p} tabprefix &c&l[Baskan] &e && tab player {p} tagprefix &c&l[Baskan] &e && title @a title {\"text\":\"👑 YENİ CUMHURBAŞKANI SEÇİLDİ!\",\"color\":\"gold\",\"bold\":true} && title @a subtitle {\"text\":\"Tebrikler {p}!\",\"color\":\"yellow\"} && broadcast &8[&4Seçim Sonucu&8] &eHalkın hür iradesiyle &c&l{p} &eyeni &4&lCumhurbaşkanı &eseçilmiştir! Kutlarız! && playsound minecraft:ui.toast.challenge_complete master @a",
         "Seçim sonucunu açıklar, oyuncuyu resmi Cumhurbaşkanı ilan eder ve tabelasını/tagını verir"),

        ("🏡 Seçim Sonucu: {p} Köy Muhtarı Seçildi!",
         "team join muhtar {p} && tab player {p} tabprefix &6&l[Muhtar] &f && tab player {p} tagprefix &6&l[Muhtar] &f && title @a title {\"text\":\"🏡 YENİ KÖY MUHTARI SEÇİLDİ!\",\"color\":\"green\",\"bold\":true} && title @a subtitle {\"text\":\"Tebrikler {p}!\",\"color\":\"yellow\"} && broadcast &8[&6Seçim Sonucu&8] &eKöy halkının oylarıyla &6&l{p} &eyeni &a&lKöy Muhtarı &eseçilmiştir! && playsound minecraft:entity.player.levelup master @a",
         "Seçim sonucunu açıklar, oyuncuyu resmi Köy Muhtarı ilan eder"),

        ("🎁 Tüm Vatandaşlara 500 Akçe Seçim Teşvik Yardımı",
         "eco give @a 500 && broadcast &a[Hazine] Seçimlere katılan tüm vatandaşlarımızın hesabına 500 Akçe yatırılmıştır! && playsound minecraft:entity.experience_orb.pickup master @a",
         "Tüm online oyuncuların banka hesabına 500 Akçe seçim katılım ödülü aktarır"),

        ("🔒 Seçimleri Tamamla & Sandıkları Kilitle",
         "broadcast &c&l[SEÇİM] Oy verme süresi sona ermiştir. Sandıklar kilitlenmiştir! && playsound minecraft:block.chest.locked master @a",
         "Seçimleri resmen kapatır ve sandıkları mühürler")
    ],

    # -------------------------------------------------------------------------
    # 21. AİRDROP & GÖKTEN KASA EVENTİ
    # -------------------------------------------------------------------------
    "🪂 AİRDROP & GÖKTEN KASA": [
        ("🪂 Hedef Konuma Airdrop İndir (İşaret Fişeği + Lüks Sandık)",
         "execute at {p} run setblock ~ ~-1 ~ beacon && execute at {p} run fill ~-1 ~-2 ~-1 ~1 ~-2 ~1 iron_block && execute at {p} run setblock ~ ~ ~ barrel{CustomName:'{\"text\":\"🪂 EFSANEVİ AİRDROP KASASI\",\"color\":\"gold\",\"bold\":true}',Items:[{Slot:0b,id:\"diamond_block\",Count:16b},{Slot:1b,id:\"netherite_ingot\",Count:8b},{Slot:2b,id:\"golden_apple\",Count:32b},{Slot:3b,id:\"totem_of_undying\",Count:2b},{Slot:4b,id:\"emerald_block\",Count:32b},{Slot:5b,id:\"experience_bottle\",Count:64b}]} && execute at {p} run summon firework_rocket ~ ~2 ~ {FireworksItem:{id:\"firework_rocket\",Count:1,tag:{Fireworks:{Flight:2,Explosions:[{Type:1,Flicker:1,Trail:1,Colors:[I;16711680,16766720],FadeColors:[I;16777215]}]}}}} && broadcast &e&l======================================== && broadcast &c&l🪂 [AİRDROP] GÖKTEN ZENGİNLİK KASASI DÜŞTÜ! && broadcast &6📍 Işın sütunu ve havai fişekler patlatıldı! İlk açan ganimeti kapar! && broadcast &e&l======================================== && playsound minecraft:ui.toast.challenge_complete master @a",
         "Hedef oyuncunun yanına ışın sütunu ve içinde 16 elmas blok, 8 netherite ve 32 altın elma olan Airdrop kasası indirir"),

        ("💥 Küçük Hızlı Airdrop Düşür (Hazine Sandığı)",
         "execute at {p} run setblock ~ ~ ~ chest{CustomName:'{\"text\":\"🎁 HIZLI AİRDROP\",\"color\":\"aqua\",\"bold\":true}',Items:[{Slot:0b,id:\"diamond\",Count:32b},{Slot:1b,id:\"emerald\",Count:64b},{Slot:2b,id:\"iron_ingot\",Count:64b},{Slot:3b,id:\"cooked_beef\",Count:64b}]} && execute at {p} run summon firework_rocket ~ ~1 ~ && broadcast &b[Airdrop] Yakınına hızlı yardım sandığı indi! && playsound minecraft:entity.player.levelup master {p}",
         "Oyuncunun hemen önüne orta boy elmas ve zümrüt airdrop sandığı bırakır"),

        ("💎 5.000 Akçe Airdrop Hediye Çeki Bırak",
         "minecraft:give {p} paper{display:{Name:'{\"text\":\"💰 5.000 AKÇE AİRDROP ÇEKİ\",\"color\":\"gold\",\"bold\":true}',Lore:['{\"text\":\"Bankaya götürerek veya admin\",\"color\":\"yellow\"}','{\"text\":\"paneli ile 5000 Akçeye çevrilir!\",\"color\":\"gray\"}']}} 1 && playsound minecraft:entity.experience_orb.pickup master {p}",
         "Hedef oyuncuya resmi airdrop altın hediye çeki verir"),

        ("🎆 Devasa Airdrop Kutlama Şovu Başlat",
         "execute at {p} run summon firework_rocket ~ ~1 ~ {FireworksItem:{id:\"firework_rocket\",Count:1,tag:{Fireworks:{Flight:3,Explosions:[{Type:2,Colors:[I;16711680,65280,255]}]}}}} && execute at {p} run summon firework_rocket ~3 ~1 ~ {FireworksItem:{id:\"firework_rocket\",Count:1,tag:{Fireworks:{Flight:2,Explosions:[{Type:1,Colors:[I;16776960]}]}}}} && broadcast &a[Airdrop] Gökyüzünde kutlama fişekleri patlatıldı! && playsound minecraft:entity.firework_rocket.blast master @a",
         "Renkli gökyüzü havai fişekleri fırlatır"),

        ("🎁 Tüm Sunucuya Airdrop Katılım Bonusu (+500 Akçe)",
         "eco give @a 500 && broadcast &6[Airdrop] Tüm vatandaşlarımıza 500 Akçe etkinlik primi dağıtıldı! && playsound minecraft:entity.player.levelup master @a",
         "Sunucudaki herkese 500 Akçe etkinlik bonusu verir")
    ],

    # -------------------------------------------------------------------------
    # 22. BOSS ZİNDANI & KANLI AY EVENTİ
    # -------------------------------------------------------------------------
    "⚔️ BOSS ZİNDANI & KANLI AY": [
        ("🩸 KANLI AY EVENTİ BAŞLAT (Zombiler Güçlenir)",
         "time set 18000 && weather thunder && broadcast &4&l======================================== && broadcast &c&l🩸 [KANLI AY] GÖKYÜZÜ KAN KIZILINA BÜRÜNDÜ! && broadcast &4Tüm zombiler ve canavarlar uyandı! Kendinizi koruyun! && broadcast &4&l======================================== && title @a title {\"text\":\"🩸 KANLI AY BAŞLADI!\",\"color\":\"dark_red\",\"bold\":true} && title @a subtitle {\"text\":\"Sığınaklarınıza çekilin!\",\"color\":\"red\"} && playsound minecraft:entity.wither.spawn master @a",
         "Geceyi kan kırmızısı yapar, yıldırımlar düşürür ve tüm oyunculara acil savunma alarmı çalar"),

        ("☀️ Kanlı Ayı Sonlandır & Güneş Doğsun",
         "time set day && weather clear && broadcast &a&l[HUZUR] Kanlı Ay sona erdi. Güneş yeniden doğdu! && title @a title {\"text\":\"☀️ GÜNEŞ DOĞDU\",\"color\":\"gold\",\"bold\":true} && playsound minecraft:ui.toast.challenge_complete master @a",
         "Kanlı Ayı bitirir, gökyüzünü açar ve güneşi doğurur"),

        ("🏰 Antik Boss Zindanı İnşa Et (11x11 Taş Tapınak)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 mossy_stone_bricks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 cracked_stone_bricks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-1 ~ ~-5 ~1 ~2 ~-5 iron_bars && execute at {p} run setblock ~ ~ ~ spawner{SpawnData:{entity:{id:\"minecraft:zombie\"}}} && execute at {p} run setblock ~ ~ ~ chest{CustomName:'{\"text\":\"🏆 ZİNDAN HAZİNESİ\",\"color\":\"gold\",\"bold\":true}',Items:[{Slot:0b,id:\"diamond\",Count:32b},{Slot:1b,id:\"netherite_scrap\",Count:4b},{Slot:2b,id:\"enchanted_golden_apple\",Count:4b}]} && execute at {p} run setblock ~-4 ~2 ~-4 soul_torch && execute at {p} run setblock ~4 ~2 ~4 soul_torch && playsound minecraft:block.stone.place master {p}",
         "Oyuncunun bulunduğu yere yosunlu taşlardan antik bir zindan odası, spawner ve hazine sandığı inşa eder"),

        ("👑 Zindan Lordu Boss'u Çağır (Netherite Zırhlı & Keskin Kılıç)",
         "execute at {p} run summon zombie ~ ~ ~ {CustomName:'{\"text\":\"👑 ZİNDAN LORDU (BOSS)\",\"color\":\"dark_red\",\"bold\":true}',CustomNameVisible:1b,Health:150f,Attributes:[{Name:\"generic.max_health\",Base:150f},{Name:\"generic.attack_damage\",Base:12f},{Name:\"generic.movement_speed\",Base:0.32f}],HandItems:[{id:\"netherite_sword\",Count:1b,tag:{Enchantments:[{id:\"sharpness\",lvl:5s}]}},{}],ArmorItems:[{id:\"netherite_boots\",Count:1b},{id:\"netherite_leggings\",Count:1b},{id:\"netherite_chestplate\",Count:1b},{id:\"diamond_helmet\",Count:1b}]} && broadcast &4[BOSS] Zindan Lordu uyandı! && playsound minecraft:entity.ender_dragon.growl master @a",
         "150 cana sahip, özel zırhlı ve elmas miğferli güçlü bir zindan bossu çağırır"),

        ("🧟 Elit Zombi Baskını Çağır (6 Zombi)",
         "execute at {p} run summon zombie ~2 ~ ~ {HandItems:[{id:\"iron_sword\",Count:1b},{}]} && execute at {p} run summon zombie ~-2 ~ ~ {HandItems:[{id:\"iron_sword\",Count:1b},{}]} && execute at {p} run summon zombie ~ ~ ~2 {HandItems:[{id:\"iron_axe\",Count:1b},{}]} && execute at {p} run summon zombie ~ ~ ~-2 && playsound minecraft:entity.zombie.ambient master {p}",
         "Hedef oyuncunun etrafına 4 silahlı zombi muhafız çağırır"),

        ("🏹 Alevli İskelet Okçu Timi Çağır",
         "execute at {p} run summon skeleton ~3 ~ ~ {HandItems:[{id:\"bow\",Count:1b,tag:{Enchantments:[{id:\"flame\",lvl:1s}]}},{}]} && execute at {p} run summon skeleton ~-3 ~ ~ {HandItems:[{id:\"bow\",Count:1b,tag:{Enchantments:[{id:\"power\",lvl:3s}]}},{}]} && playsound minecraft:entity.skeleton.ambient master {p}",
         "Alev okları atan 2 iskelet nişancı çağırır"),

        ("🏆 Zindan Zaferi & Boss Ödülü (+2.000 Akçe)",
         "eco give @a 2000 && broadcast &6&l🏆 [ZAFER] Zindan Boss'u devrildi! Tüm savaşçılara 2.000 Akçe ödül verildi! && playsound minecraft:ui.toast.challenge_complete master @a",
         "Boss'u yenen tüm oyunculara 2.000 Akçe zafer ödülü dağıtır")
    ],

    # -------------------------------------------------------------------------
    # 23. KLANLAR & KRALLIK SAVAŞLARI
    # -------------------------------------------------------------------------
    "🏰 KLANLAR & KRALLIK SAVAŞLARI": [
        ("🚩 Kızıl Bayrak Klanını Kur",
         "team add klan_kizil \"Kızıl Bayrak Klanı\" && team modify klan_kizil prefix \"&c[Kızıl] \" && team modify klan_kizil color red && team modify klan_kizil friendlyFire false && broadcast &c[Klan] Kızıl Bayrak Klanı resmen kuruldu! && playsound minecraft:entity.player.levelup master @a",
         "Kızıl Bayrak adında kırmızı renkli ve dost ateşi kapalı bir klan kurar"),

        ("🐺 Kurtlar Hanedanı Klanını Kur",
         "team add klan_kurtlar \"Kurtlar Hanedanı\" && team modify klan_kurtlar prefix \"&6[Kurtlar] \" && team modify klan_kurtlar color gold && team modify klan_kurtlar friendlyFire false && broadcast &6[Klan] Kurtlar Hanedanı klanı kuruldu! && playsound minecraft:entity.player.levelup master @a",
         "Altın sarısı renkli Kurtlar Hanedanı klanını kurar"),

        ("🦅 Kartal Krallığı Klanını Kur",
         "team add klan_kartal \"Kartal Krallığı\" && team modify klan_kartal prefix \"&9[Kartal] \" && team modify klan_kartal color blue && team modify klan_kartal friendlyFire false && broadcast &9[Klan] Kartal Krallığı klanı kuruldu! && playsound minecraft:entity.player.levelup master @a",
         "Mavi renkli Kartal Krallığı klanını kurar"),

        ("➕ {p} Oyuncusunu Kızıl Bayrak Klanına Ekle",
         "team join klan_kizil {p} && broadcast &c[Klan] {p} Kızıl Bayrak klanına katıldı! && playsound minecraft:entity.experience_orb.pickup master {p}",
         "Seçili oyuncuyu Kızıl Bayrak klanına üye yapar"),

        ("➕ {p} Oyuncusunu Kurtlar Hanedanına Ekle",
         "team join klan_kurtlar {p} && broadcast &6[Klan] {p} Kurtlar Hanedanına katıldı! && playsound minecraft:entity.experience_orb.pickup master {p}",
         "Seçili oyuncuyu Kurtlar Hanedanına üye yapar"),

        ("➕ {p} Oyuncusunu Kartal Krallığına Ekle",
         "team join klan_kartal {p} && broadcast &9[Klan] {p} Kartal Krallığına katıldı! && playsound minecraft:entity.experience_orb.pickup master {p}",
         "Seçili oyuncuyu Kartal Krallığına üye yapar"),

        ("❌ {p} Oyuncusunu Klandan Çıkar",
         "team leave {p} && broadcast &7[Klan] {p} klanından ayrıldı. && playsound minecraft:block.anvil.land master {p}",
         "Oyuncuyu bulunduğu klandan çıkarır"),

        ("⚔️ BÜYÜK KLAN SAVAŞI BAŞLAT! (PvP Meydanı)",
         "broadcast &4&l======================================== && broadcast &c&l⚔️ KRALLIKLAR ARASI BÜYÜK KLAN SAVAŞI BAŞLADI! && broadcast &eTüm klanlar PvP Arenasında kozlarını paylaşıyor! && broadcast &4&l======================================== && title @a title {\"text\":\"⚔️ KLAN SAVAŞI BAŞLADI!\",\"color\":\"red\",\"bold\":true} && playsound minecraft:entity.ender_dragon.growl master @a",
         "Sunucu genelinde klanlar arası büyük meydan savaşı başlatır"),

        ("💰 Klan Hazinesi Bonusu Ver (+10.000 Akçe)",
         "eco give {p} 10000 && broadcast &e[Hazine] {p} klan hazinesine 10.000 Akçe aktarıldı! && playsound minecraft:entity.player.levelup master {p}",
         "Klan liderine klanı büyütmesi için 10.000 Akçe verir")
    ],

    # -------------------------------------------------------------------------
    # 24. HOLOGRAMLAR & LİDERLİK TABLOSU
    # -------------------------------------------------------------------------
    "🏆 HOLOGRAMLAR & LİDERLİK TABLOSU": [
        ("🏆 Liderlik Kürsüsü Hologramını Buraya Taşı",
         "execute at {p} run dh movehere liderlik_tablosu && playsound minecraft:entity.player.levelup master {p}",
         "En zengin oyuncular liderlik tablosunu hedef oyuncunun tam karşısına taşır"),

        ("📜 Sunucu Rehber Hologramını Buraya Taşı",
         "execute at {p} run dh movehere spawn_rehber && playsound minecraft:entity.player.levelup master {p}",
         "Sunucu kuralları ve başlangıç rehberi hologramını hedef oyuncunun yanına taşır"),

        ("🔄 Tüm Hologramları Yenile (/dh reload)",
         "dh reload && playsound minecraft:entity.experience_orb.pickup master {p}",
         "DecentHolograms eklentisini ve canlı tabloları günceller"),

        ("✨ Günlük Görevler & Ödül Dağıt (+500 Akçe & 5 Elmas)",
         "eco give {p} 500 && minecraft:give {p} diamond 5 && minecraft:give {p} cooked_beef 32 && broadcast &a[Görev] {p} bugünkü görevlerini tamamlayıp ödülünü aldı! && playsound minecraft:ui.toast.challenge_complete master {p}",
         "Hedef oyuncuya günlük görev ödül paketini (+500 Akçe, 5 Elmas, 32 Pişmiş Biftek) verir"),

        ("🌟 Tüm Sunucuya Görev Teşvik Bonusu Dağıt (+250 Akçe)",
         "eco give @a 250 && broadcast &e[Görevler] Günlük görevlere katılan tüm oyunculara 250 Akçe prim dağıtıldı! && playsound minecraft:entity.experience_orb.pickup master @a",
         "Online olan herkese 250 Akçe görev tamamlama primi dağıtır")
    ]
}

# rom1504/minecraft-schematics-dataset Kategorilerini TABS_DATA'nın Başına Entegre Et
if schematics_manager and hasattr(schematics_manager, "SCHEMATIC_TABS"):
    _UPDATED_TABS_DATA = {}
    for _k, _v in schematics_manager.SCHEMATIC_TABS.items():
        _UPDATED_TABS_DATA[_k] = _v
    for _k, _v in TABS_DATA.items():
        if _k not in _UPDATED_TABS_DATA:
            _UPDATED_TABS_DATA[_k] = _v
    TABS_DATA = _UPDATED_TABS_DATA


# =============================================================================
# GUI ARAYÜZÜ (Modern Dark Cyberpunk Tasarımı)
# =============================================================================
class AdminGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ MINECRAFT FORGE 1.20.1 ULTIMATE PRO ADMIN & BUILD MASTER PANEL")
        self.root.geometry("1340x940")
        self.root.minsize(920, 620)
        self.cols = 3
        self.category_buttons = {}
        self.all_button_cards = []
        self.selected_category = tk.StringVar(value=list(TABS_DATA.keys())[0])

        # Renk Paleti (Deep Slate Dark + Neon Cyan + Emerald + Gold + Crimson)
        self.BG_DARK = "#090d16"
        self.BG_PANEL = "#0f172a"
        self.BG_CARD = "#1e293b"
        self.BG_HOVER = "#334155"
        self.BORDER_COLOR = "#334155"
        self.TEXT_COLOR = "#f8fafc"
        self.TEXT_MUTED = "#94a3b8"
        self.ACCENT_CYAN = "#38bdf8"
        self.ACCENT_GREEN = "#10b981"
        self.ACCENT_GOLD = "#f59e0b"
        self.ACCENT_PURPLE = "#a855f7"
        self.ACCENT_RED = "#ef4444"

        self.root.configure(bg=self.BG_DARK)
        self.rcon = MinecraftRcon()
        self.command_history = []
        self.history_index = -1
        self.log_pos = 0
        self.all_button_cards = []

        # Arka plan ayarları
        self.running = True
        self.autosave_enabled = True
        self.salary_enabled = tk.BooleanVar(value=False)
        self.salary_amount = tk.StringVar(value="250")

        self._apply_styles()
        self._build_header()
        self._build_quick_action_ribbon()
        self._build_universal_block_hub()
        self._build_tabs_section()
        self._build_console_section()

        # Arka plan iş parçacıkları
        self.log_thread = threading.Thread(target=self._tail_log_thread, daemon=True)
        self.log_thread.start()

        self.status_thread = threading.Thread(target=self._status_monitor_thread, daemon=True)
        self.status_thread.start()

        self.autosave_thread = threading.Thread(target=self._autosave_worker, daemon=True)
        self.autosave_thread.start()

        self.salary_thread = threading.Thread(target=self._salary_worker, daemon=True)
        self.salary_thread.start()

        self.lan_thread = threading.Thread(target=self._lan_broadcast_worker, daemon=True)
        self.lan_thread.start()

        self.broadcast_thread = threading.Thread(target=self._announcement_worker, daemon=True)
        self.broadcast_thread.start()

        threading.Thread(target=self.update_player_dropdown, daemon=True).start()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=self.BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.BG_CARD, foreground=self.TEXT_COLOR,
                        padding=[10, 6], font=("Segoe UI", 8, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", self.ACCENT_CYAN), ("active", self.BG_HOVER)],
                  foreground=[("selected", "#000000"), ("active", "#ffffff")])

        style.configure("TCombobox", fieldbackground=self.BG_CARD, background=self.BG_CARD,
                        foreground=self.TEXT_COLOR, arrowcolor=self.ACCENT_CYAN, borderwidth=0)

    def _build_header(self):
        header = tk.Frame(self.root, bg=self.BG_PANEL, height=52, padx=14, pady=6)
        header.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header,
            text="⚔️ MINECRAFT ULTIMATE PRO & BUILD MASTER PANEL",
            font=("Segoe UI", 11, "bold"),
            fg=self.ACCENT_GOLD,
            bg=self.BG_PANEL
        )
        title_lbl.pack(side=tk.LEFT)

        self.status_lbl = tk.Label(
            header,
            text="● KONTROL EDILIYOR...",
            font=("Segoe UI", 8, "bold"),
            fg=self.ACCENT_GOLD,
            bg="#2a2312",
            padx=8,
            pady=3
        )
        self.status_lbl.pack(side=tk.LEFT, padx=10)

        ip_lbl = tk.Label(
            header,
            text=f"🌐 Yerel Ağ: {get_local_ip()} | Port: {SERVER_PORT}",
            font=("Segoe UI", 8, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_PANEL
        )
        ip_lbl.pack(side=tk.LEFT, padx=6)

        btn_stop = tk.Button(
            header,
            text="⏹️ Sunucuyu Kapat",
            font=("Segoe UI", 8, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=2,
            command=self.stop_server
        )
        btn_stop.pack(side=tk.RIGHT, padx=3)

        btn_start = tk.Button(
            header,
            text="▶️ Sunucuyu Başlat",
            font=("Segoe UI", 8, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=2,
            command=self.start_server
        )
        btn_start.pack(side=tk.RIGHT, padx=3)

        btn_builder = tk.Button(
            header,
            text="🚀 Auto Server Maker & AI Hub",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=2,
            command=self.open_auto_server_maker
        )
        btn_builder.pack(side=tk.RIGHT, padx=5)

    # =========================================================================
    # HIZLI KONTROL & AKSIYON ÇUBUĞU (Quick Action Ribbon)
    # =========================================================================
    def _build_quick_action_ribbon(self):
        ribbon = tk.Frame(self.root, bg="#0d1424", padx=10, pady=4)
        ribbon.pack(fill=tk.X, side=tk.TOP)

        # 1. Satır: Hedef Oyuncu, Adet, Rol Seçimi ve Yedek
        row1 = tk.Frame(ribbon, bg="#0d1424")
        row1.pack(fill=tk.X, pady=(0, 3))

        lbl_p = tk.Label(row1, text="🎯 Hedef:", font=("Segoe UI", 8, "bold"), fg=self.TEXT_COLOR, bg="#0d1424")
        lbl_p.pack(side=tk.LEFT, padx=(0, 4))

        self.player_var = tk.StringVar(value="MIRKUNDAKLAYAN")
        self.player_entry = ttk.Combobox(
            row1,
            textvariable=self.player_var,
            font=("Segoe UI", 8, "bold"),
            width=15,
            values=["MIRKUNDAKLAYAN", "@a", "@p"]
        )
        self.player_entry.pack(side=tk.LEFT, padx=(0, 2))

        btn_refresh_p = tk.Button(
            row1,
            text="🔄",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg="#38bdf8",
            activebackground="#334155",
            activeforeground="#38bdf8",
            relief=tk.FLAT,
            padx=4,
            pady=1,
            command=lambda: threading.Thread(target=self.update_player_dropdown, daemon=True).start()
        )
        btn_refresh_p.pack(side=tk.LEFT, padx=(0, 6))

        lbl_q = tk.Label(row1, text="🔢 Adet:", font=("Segoe UI", 8, "bold"), fg=self.TEXT_COLOR, bg="#0d1424")
        lbl_q.pack(side=tk.LEFT, padx=(0, 4))

        self.qty_var = tk.StringVar(value="64")
        self.qty_entry = ttk.Combobox(
            row1,
            textvariable=self.qty_var,
            font=("Segoe UI", 8, "bold"),
            width=4,
            values=["1", "16", "32", "64", "128", "256", "576"]
        )
        self.qty_entry.pack(side=tk.LEFT, padx=(0, 4))

        lbl_akce = tk.Label(row1, text="💰 Akçe:", font=("Segoe UI", 8, "bold"), fg=self.ACCENT_GOLD, bg="#0d1424")
        lbl_akce.pack(side=tk.LEFT, padx=(2, 2))

        self.akce_var = tk.StringVar(value="50000")
        self.akce_entry = ttk.Combobox(
            row1,
            textvariable=self.akce_var,
            font=("Segoe UI", 8, "bold"),
            width=7,
            values=["500", "1000", "5000", "10000", "50000", "100000", "250000", "500000", "1000000"]
        )
        self.akce_entry.pack(side=tk.LEFT, padx=(0, 2))

        btn_give_akce = tk.Button(
            row1,
            text="➕ Yükle",
            font=("Segoe UI", 8, "bold"),
            bg="#10b981",
            fg="white",
            relief=tk.FLAT,
            padx=4,
            pady=1,
            command=lambda: self.run_custom_template("eco give {p} {akce} && scoreboard players add {p} akce {akce} && title {p} actionbar {\"text\":\"💰 +{akce} Akçe Yüklendi!\",\"color\":\"green\"}")
        )
        btn_give_akce.pack(side=tk.LEFT, padx=1)

        btn_take_akce = tk.Button(
            row1,
            text="➖ Kes",
            font=("Segoe UI", 8, "bold"),
            bg="#ef4444",
            fg="white",
            relief=tk.FLAT,
            padx=4,
            pady=1,
            command=lambda: self.run_custom_template("eco take {p} {akce} && scoreboard players remove {p} akce {akce} && title {p} actionbar {\"text\":\"💸 -{akce} Akçe Kesildi!\",\"color\":\"red\"}")
        )
        btn_take_akce.pack(side=tk.LEFT, padx=1)

        btn_set_akce = tk.Button(
            row1,
            text="🎯 Sabitle",
            font=("Segoe UI", 8, "bold"),
            bg="#3b82f6",
            fg="white",
            relief=tk.FLAT,
            padx=4,
            pady=1,
            command=lambda: self.run_custom_template("eco set {p} {akce} && scoreboard players set {p} akce {akce} && title {p} actionbar {\"text\":\"🎯 Bakiye: {akce} Akçe Olarak Güncellendi!\",\"color\":\"gold\"}")
        )
        btn_set_akce.pack(side=tk.LEFT, padx=(1, 4))

        lbl_r = tk.Label(row1, text="🎭 Rol:", font=("Segoe UI", 8, "bold"), fg=self.ACCENT_GOLD, bg="#0d1424")
        lbl_r.pack(side=tk.LEFT, padx=(2, 4))

        self.roles_dict = {
            "👑 Cumhurbaşkanı": ("cumhurbaskani", "&c&l[Baskan] &e", "👑 CUMHURBAŞKANI SEÇİLDİNİZ!"),
            "🏡 Köy Muhtarı": ("muhtar", "&6&l[Muhtar] &f", "🏡 KÖY MUHTARI OLDUNUZ!"),
            "👮 Polis Memuru": ("polis", "&9&l[Polis] &b", "👮 POLİS MEMURU OLDUNUZ!"),
            "🪖 Asker & Komutan": ("asker", "&2&l[Asker] &a", "🪖 ASKER OLDUNUZ!"),
            "🩺 Doktor / Hekim": ("doktor", "&c&l[Doktor] &f", "🩺 DOKTOR OLDUNUZ!"),
            "⚖️ Ağır Ceza Hakimi": ("hakim", "&5&l[Hakim] &d", "⚖️ HAKİM OLDUNUZ!"),
            "🏗️ Baş Mimar": ("mimar", "&3&l[Mimar] &b", "🏗️ BAŞ MİMAR OLDUNUZ!"),
            "💰 Büyük Tüccar": ("tuccar", "&e&l[Tuccar] &6", "💰 BÜYÜK TÜCCAR OLDUNUZ!"),
            "⛏️ Usta Madenci": ("madenci", "&8&l[Madenci] &7", "⛏️ MADENCİ OLDUNUZ!"),
            "🌾 Baş Çiftçi": ("ciftci", "&a&l[Ciftci] &2", "🌾 ÇİFTÇİ OLDUNUZ!"),
            "⚔️ Kraliyet Şövalyesi": ("sovalye", "&1&l[Sovalye] &9", "⚔️ KRALİYET ŞÖVALYESİ OLDUNUZ!"),
            "👑 Kurucu / Kral": ("kurucu", "&4&l[Kurucu] &c", "👑 SUNUCU KURUCUSU / KRAL!"),
            "❌ Vatandaş (Sıfırla)": ("vatandas", "&7[Vatandas] &f", "Standart Vatandaş")
        }

        self.role_var = tk.StringVar(value=list(self.roles_dict.keys())[0])
        self.role_combo = ttk.Combobox(
            row1,
            textvariable=self.role_var,
            font=("Segoe UI", 8, "bold"),
            width=14,
            values=list(self.roles_dict.keys()),
            state="readonly"
        )
        self.role_combo.pack(side=tk.LEFT, padx=(0, 2))

        btn_assign_role = tk.Button(
            row1,
            text="👑 Rolü Ata",
            font=("Segoe UI", 8, "bold"),
            bg="#f59e0b",
            fg="#000000",
            activebackground="#d97706",
            activeforeground="#000000",
            relief=tk.FLAT,
            padx=5,
            pady=1,
            command=self.assign_selected_role
        )
        btn_assign_role.pack(side=tk.LEFT, padx=(0, 8))

        btn_box = tk.Button(
            row1,
            text="📦 3'lü God Kit",
            font=("Segoe UI", 8, "bold"),
            bg=self.ACCENT_PURPLE,
            fg="white",
            relief=tk.FLAT,
            padx=6,
            command=lambda: self.run_custom_template(CMD_COMBO_FULL)
        )
        btn_box.pack(side=tk.LEFT, padx=2)

        btn_backup = tk.Button(
            row1,
            text="💾 Dünya Yedeği Al",
            font=("Segoe UI", 8, "bold"),
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            relief=tk.FLAT,
            padx=6,
            command=self.create_world_backup
        )
        btn_backup.pack(side=tk.LEFT, padx=2)

        # 2. Satır: Hızlı Buff Butonları & Maaş & Arama
        row2 = tk.Frame(ribbon, bg="#0d1424")
        row2.pack(fill=tk.X)

        quick_btns = [
            ("⚡ God Mode", "effect give {p} resistance 99999 5 true && effect give {p} strength 99999 50 true", self.ACCENT_GOLD, "#000000"),
            ("💖 Full Can", "effect give {p} instant_health 1 255 true && effect give {p} saturation 1 255 true", self.ACCENT_GREEN, "#000000"),
            ("🕊️ Fly", "gamemode creative {p}", "#0284c7", "#ffffff"),
            ("🍖 Doyur", "feed {p} && effect give {p} saturation 1 10 true", "#d97706", "#ffffff"),
            ("🧹 Lag Temizle", "minecraft:kill @e[type=item]", self.ACCENT_RED, "#ffffff"),
            ("💾 Kaydet", "save-all flush", "#4b5563", "#ffffff")
        ]
        for name, cmd, bg_col, fg_col in quick_btns:
            b = tk.Button(
                row2,
                text=name,
                font=("Segoe UI", 8, "bold"),
                bg=bg_col,
                fg=fg_col,
                relief=tk.FLAT,
                padx=5,
                pady=1,
                command=lambda c=cmd: self.run_custom_template(c)
            )
            b.pack(side=tk.LEFT, padx=2)

        chk_sal = tk.Checkbutton(
            row2,
            text="💰 Oto-Maaş (10dk)",
            variable=self.salary_enabled,
            font=("Segoe UI", 8, "bold"),
            fg=self.ACCENT_GOLD,
            bg="#0d1424",
            activebackground="#0d1424",
            activeforeground=self.ACCENT_GOLD,
            selectcolor="#1e293b"
        )
        chk_sal.pack(side=tk.LEFT, padx=(8, 2))

        ent_sal = tk.Entry(
            row2,
            textvariable=self.salary_amount,
            font=("Consolas", 8, "bold"),
            width=5,
            bg=self.BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        ent_sal.pack(side=tk.LEFT, padx=(0, 6))

        lbl_s = tk.Label(row2, text="🔍 Arama:", font=("Segoe UI", 8, "bold"), fg=self.TEXT_COLOR, bg="#0d1424")
        lbl_s.pack(side=tk.LEFT, padx=(4, 2))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            row2,
            textvariable=self.search_var,
            font=("Segoe UI", 8),
            bg=self.BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            width=18
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2), ipady=2)
        self.search_var.trace_add("write", self._on_search_change)

    # =========================================================================
    # GELİŞMİŞ BLOK DAĞITIM MERKEZİ (Universal Block Spawner Hub)
    # =========================================================================
    def _build_universal_block_hub(self):
        hub_frame = tk.Frame(self.root, bg="#111827", padx=14, pady=4)
        hub_frame.pack(fill=tk.X, side=tk.TOP)

        row1 = tk.Frame(hub_frame, bg="#111827")
        row1.pack(fill=tk.X, pady=(0, 3))

        lbl_cat = tk.Label(row1, text="🧱 Kategori:", font=("Segoe UI", 8, "bold"), fg=self.ACCENT_GOLD, bg="#111827")
        lbl_cat.pack(side=tk.LEFT, padx=(0, 4))

        categories = list(BLOCK_CATALOG.keys())
        self.block_cat_var = tk.StringVar(value=categories[0])
        self.block_cat_combo = ttk.Combobox(
            row1,
            textvariable=self.block_cat_var,
            font=("Segoe UI", 8, "bold"),
            width=18,
            values=categories,
            state="readonly"
        )
        self.block_cat_combo.pack(side=tk.LEFT, padx=(0, 6))
        self.block_cat_combo.bind("<<ComboboxSelected>>", self._on_block_category_change)

        lbl_blk = tk.Label(row1, text="📦 Blok:", font=("Segoe UI", 8, "bold"), fg=self.ACCENT_CYAN, bg="#111827")
        lbl_blk.pack(side=tk.LEFT, padx=(0, 4))

        self.block_select_var = tk.StringVar()
        self.block_select_combo = ttk.Combobox(
            row1,
            textvariable=self.block_select_var,
            font=("Segoe UI", 8),
            width=22,
            state="readonly"
        )
        self.block_select_combo.pack(side=tk.LEFT, padx=(0, 6))
        self.block_select_combo.bind("<<ComboboxSelected>>", self._on_block_selected_from_catalog)

        lbl_id = tk.Label(row1, text="✍️ ID:", font=("Segoe UI", 8, "bold"), fg=self.TEXT_COLOR, bg="#111827")
        lbl_id.pack(side=tk.LEFT, padx=(0, 4))

        self.custom_item_var = tk.StringVar(value="minecraft:barrier")
        self.custom_item_entry = tk.Entry(
            row1,
            textvariable=self.custom_item_var,
            font=("Consolas", 8),
            bg=self.BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            width=20
        )
        self.custom_item_entry.pack(side=tk.LEFT, padx=(0, 6), ipady=2)
        self.custom_item_entry.bind("<Return>", lambda e: self.dispatch_block("give"))

        # İşlem Butonları
        btn_give = tk.Button(
            row1,
            text="🚀 Envantere Ver",
            font=("Segoe UI", 8, "bold"),
            bg=self.ACCENT_GREEN,
            fg="#000000",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.dispatch_block("give")
        )
        btn_give.pack(side=tk.LEFT, padx=2)

        btn_setunder = tk.Button(
            row1,
            text="🦶 Ayak Altına",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.dispatch_block("setblock_under")
        )
        btn_setunder.pack(side=tk.LEFT, padx=2)

        btn_wall = tk.Button(
            row1,
            text="🧱 3x3 Duvar",
            font=("Segoe UI", 8, "bold"),
            bg=self.ACCENT_GOLD,
            fg="#000000",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.dispatch_block("wall_front")
        )
        btn_wall.pack(side=tk.LEFT, padx=2)

        btn_box_wrap = tk.Button(
            row1,
            text="🕳️ Kutu Yap",
            font=("Segoe UI", 8, "bold"),
            bg=self.ACCENT_PURPLE,
            fg="#ffffff",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.dispatch_block("box_outline")
        )
        btn_box_wrap.pack(side=tk.LEFT, padx=2)

        btn_platform = tk.Button(
            row1,
            text="🌟 5x5 Platform",
            font=("Segoe UI", 8, "bold"),
            bg="#0d9488",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.dispatch_block("platform")
        )
        btn_platform.pack(side=tk.LEFT, padx=2)

        # Favoriler Satırı
        row2 = tk.Frame(hub_frame, bg="#111827")
        row2.pack(fill=tk.X)

        lbl_fav = tk.Label(row2, text="⚡ Favoriler:", font=("Segoe UI", 7, "bold"), fg=self.TEXT_MUTED, bg="#111827")
        lbl_fav.pack(side=tk.LEFT, padx=(0, 4))

        favorites = [
            ("🚫 Barrier", "barrier"),
            ("⚡ Komut Bloğu", "command_block"),
            ("💡 Işık 15", "light[level=15]"),
            ("⬛ Bedrock", "bedrock"),
            ("👾 Spawner", "spawner"),
            ("🌌 Antik Kalıntı", "ancient_debris"),
            ("🧱 Netherite", "netherite_block"),
            ("💎 Elmas", "diamond_block"),
            ("🏛️ Kuvars", "smooth_quartz"),
            ("🌊 Deniz Feneri", "sea_lantern"),
            ("🪟 Karartılmış Cam", "tinted_glass"),
            ("🧊 Mavi Buz", "blue_ice"),
            ("🧨 TNT", "tnt")
        ]
        for name, item_id in favorites:
            btn_h = tk.Button(
                row2,
                text=name,
                font=("Segoe UI", 7),
                bg=self.BG_CARD,
                fg=self.TEXT_MUTED,
                activebackground=self.BG_HOVER,
                activeforeground="#ffffff",
                relief=tk.FLAT,
                padx=4,
                pady=1,
                command=lambda i=item_id: self.quick_select_block(i)
            )
            btn_h.pack(side=tk.LEFT, padx=2)

        self._update_block_catalog_dropdown()

    def _on_block_category_change(self, event=None):
        self._update_block_catalog_dropdown()

    def _update_block_catalog_dropdown(self):
        cat = self.block_cat_var.get()
        items = BLOCK_CATALOG.get(cat, [])
        names = [name for name, _ in items]
        self.block_select_combo.configure(values=names)
        if names:
            self.block_select_combo.current(0)
            self._on_block_selected_from_catalog()

    def _on_block_selected_from_catalog(self, event=None):
        cat = self.block_cat_var.get()
        items = BLOCK_CATALOG.get(cat, [])
        sel_idx = self.block_select_combo.current()
        if 0 <= sel_idx < len(items):
            _, raw_id = items[sel_idx]
            if not raw_id.startswith("minecraft:") and ":" not in raw_id and "{" not in raw_id and "[" not in raw_id:
                raw_id = f"minecraft:{raw_id}"
            self.custom_item_var.set(raw_id)

    def quick_select_block(self, item_id):
        if not item_id.startswith("minecraft:") and ":" not in item_id and "{" not in item_id and "[" not in item_id:
            item_id = f"minecraft:{item_id}"
        self.custom_item_var.set(item_id)
        self.dispatch_block("give")

    def dispatch_block(self, mode="give"):
        item_id = self.custom_item_var.get().strip()
        if not item_id:
            return
        if not item_id.startswith("minecraft:") and ":" not in item_id and "{" not in item_id and "[" not in item_id:
            item_id = f"minecraft:{item_id}"

        target = self.player_var.get().strip() or "@p"
        qty = self.qty_var.get().strip() or "64"

        clean_block = item_id.split("{")[0]

        if mode == "give":
            cmd = f"give {target} {item_id} {qty}"
        elif mode == "setblock_under":
            cmd = f"execute at {target} run setblock ~ ~-1 ~ {clean_block}"
        elif mode == "wall_front":
            cmd = f"execute at {target} run fill ^-1 ^ ^3 ^1 ^2 ^3 {clean_block}"
        elif mode == "box_outline":
            cmd = f"execute at {target} run fill ~-1 ~-1 ~-1 ~1 ~2 ~1 {clean_block} outline"
        elif mode == "platform":
            cmd = f"execute at {target} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 {clean_block}"
        else:
            cmd = f"give {target} {item_id} {qty}"

        self.log_console(f">> {cmd}\n", tag="cmd")
        threading.Thread(target=self._run_cmd_async, args=(cmd,), daemon=True).start()

    # =========================================================================
    # RESPONSIVE KATEGORİ GEZGİNİ & İÇERİK IZGARASI (Sidebar & Dynamic Grid)
    # =========================================================================
    def _build_tabs_section(self):
        # Ana Gövde Taşıyıcısı (Sol Sidebar + Sağ İçerik)
        self.body_container = tk.Frame(self.root, bg=self.BG_DARK)
        self.body_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # -------------------------------------------------------------
        # SOL SIDEBAR: Kategori Gezgini (Scrollable Categories)
        # -------------------------------------------------------------
        self.sidebar_frame = tk.Frame(
            self.body_container,
            bg=self.BG_PANEL,
            width=230,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        self.sidebar_frame.pack_propagate(False)

        # Sidebar Üst Başlık & Arama
        side_top = tk.Frame(self.sidebar_frame, bg=self.BG_PANEL, padx=8, pady=6)
        side_top.pack(fill=tk.X)

        side_title = tk.Label(
            side_top,
            text=f"📂 KATEGORİLER ({len(TABS_DATA)})",
            font=("Segoe UI", 9, "bold"),
            fg=self.ACCENT_GOLD,
            bg=self.BG_PANEL
        )
        side_title.pack(anchor="w", pady=(0, 4))

        self.cat_search_var = tk.StringVar()
        cat_search_ent = tk.Entry(
            side_top,
            textvariable=self.cat_search_var,
            font=("Segoe UI", 8),
            bg=self.BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        cat_search_ent.pack(fill=tk.X, ipady=2)
        cat_search_ent.insert(0, "")
        self.cat_search_var.trace_add("write", lambda *args: self._populate_sidebar_categories())

        # Sidebar Kaydırılabilir Kategori Listesi
        self.sidebar_canvas = tk.Canvas(self.sidebar_frame, bg=self.BG_PANEL, highlightthickness=0)
        self.sidebar_scrollbar = tk.Scrollbar(self.sidebar_frame, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar_buttons_frame = tk.Frame(self.sidebar_canvas, bg=self.BG_PANEL)

        self.sidebar_buttons_frame.bind(
            "<Configure>",
            lambda e: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))
        )
        self.sidebar_canvas.create_window((0, 0), window=self.sidebar_buttons_frame, anchor="nw", width=212)
        self.sidebar_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)

        self.sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0), pady=(0, 4))
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 4))

        # Fare tekerleği bağlama
        self.sidebar_canvas.bind("<Enter>", lambda e: self.sidebar_canvas.bind_all("<MouseWheel>", lambda ev: self.sidebar_canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")))
        self.sidebar_canvas.bind("<Leave>", lambda e: self.sidebar_canvas.unbind_all("<MouseWheel>"))

        self._populate_sidebar_categories()

        # -------------------------------------------------------------
        # SAĞ İÇERİK ALANI (Responsive Card Grid)
        # -------------------------------------------------------------
        self.content_area = tk.Frame(self.body_container, bg=self.BG_DARK)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sağ Alan Üst Çubuğu (Başlık + Dropdown Kategori Seçici + Kategori İçi Arama)
        content_header = tk.Frame(self.content_area, bg=self.BG_PANEL, padx=10, pady=5, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        content_header.pack(fill=tk.X, pady=(0, 4))

        self.cat_title_lbl = tk.Label(
            content_header,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_PANEL
        )
        self.cat_title_lbl.pack(side=tk.LEFT)

        # Hızlı Kategori Seçici Combobox
        lbl_jump = tk.Label(content_header, text="  ⚡ Hızlı Seç:", font=("Segoe UI", 8, "bold"), fg=self.TEXT_MUTED, bg=self.BG_PANEL)
        lbl_jump.pack(side=tk.LEFT, padx=(10, 4))

        self.category_combo = ttk.Combobox(
            content_header,
            textvariable=self.selected_category,
            font=("Segoe UI", 8, "bold"),
            values=list(TABS_DATA.keys()),
            state="readonly",
            width=26
        )
        self.category_combo.pack(side=tk.LEFT, padx=(0, 8))
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.switch_category(self.selected_category.get()))

        btn_force_refresh = tk.Button(
            content_header,
            text="🔄 Yenile",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg=self.ACCENT_CYAN,
            activebackground=self.BG_HOVER,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.switch_category(self.selected_category.get())
        )
        btn_force_refresh.pack(side=tk.LEFT, padx=3)

        btn_clear_search = tk.Button(
            content_header,
            text="❌ Aramayı Temizle",
            font=("Segoe UI", 8, "bold"),
            bg="#1e293b",
            fg=self.ACCENT_GOLD,
            activebackground=self.BG_HOVER,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=6,
            pady=1,
            command=lambda: self.search_var.set("")
        )
        btn_clear_search.pack(side=tk.LEFT, padx=3)

        # İçerik Canvas & Scrollbar
        self.content_canvas = tk.Canvas(self.content_area, bg=self.BG_DARK, highlightthickness=0, borderwidth=0)
        self.content_scrollbar = tk.Scrollbar(self.content_area, orient="vertical", command=self.content_canvas.yview)
        self.cards_frame = tk.Frame(self.content_canvas, bg=self.BG_DARK)

        self.cards_frame.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        )
        self.content_canvas_window = self.content_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)

        self.content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas resize: pencere genişliğine göre canvas window genişliğini ve sütun sayısını ayarla
        self.content_canvas.bind("<Configure>", self._on_content_canvas_resize)

        # MouseWheel for content canvas
        self.content_canvas.bind("<Enter>", lambda e: self.content_canvas.bind_all("<MouseWheel>", lambda ev: self.content_canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")))
        self.content_canvas.bind("<Leave>", lambda e: self.content_canvas.unbind_all("<MouseWheel>"))

        # İlk kategoriyi aç
        self.switch_category(self.selected_category.get())

    def _populate_sidebar_categories(self):
        for widget in self.sidebar_buttons_frame.winfo_children():
            widget.destroy()
        self.category_buttons.clear()

        filter_q = self.cat_search_var.get().lower().strip()
        current_cat = self.selected_category.get()

        for cat_name, items in TABS_DATA.items():
            if filter_q and filter_q not in cat_name.lower():
                continue

            count = len(items)
            display_text = f"{cat_name} ({count})"

            is_active = (cat_name == current_cat)
            btn = tk.Button(
                self.sidebar_buttons_frame,
                text=display_text,
                font=("Segoe UI", 8, "bold" if is_active else "normal"),
                bg=self.ACCENT_CYAN if is_active else self.BG_PANEL,
                fg="#000000" if is_active else self.TEXT_COLOR,
                activebackground=self.BG_HOVER,
                activeforeground="#ffffff",
                relief=tk.FLAT,
                anchor="w",
                padx=8,
                pady=4,
                command=lambda cn=cat_name: self.switch_category(cn)
            )
            btn.pack(fill=tk.X, padx=2, pady=1)
            self.category_buttons[cat_name] = btn

    def switch_category(self, cat_name):
        if cat_name not in TABS_DATA:
            return
        self.selected_category.set(cat_name)
        count = len(TABS_DATA[cat_name])
        self.cat_title_lbl.config(text=f"{cat_name} ({count} Öğe)")
        self.category_combo.set(cat_name)

        # Clear search filter when switching category so all items in new category appear immediately!
        if self.search_var.get():
            self.search_var.set("")

        # Highlight active sidebar button
        for cname, btn in self.category_buttons.items():
            if cname == cat_name:
                btn.config(bg=self.ACCENT_CYAN, fg="#000000", font=("Segoe UI", 8, "bold"))
            else:
                btn.config(bg=self.BG_PANEL, fg=self.TEXT_COLOR, font=("Segoe UI", 8))

        # Render cards and refresh canvas immediately
        self._render_active_cards()

    def _on_content_canvas_resize(self, event):
        canvas_width = event.width
        self.content_canvas.itemconfig(self.content_canvas_window, width=canvas_width)

        # Dinamik responsive sütun sayısı hesapla
        if canvas_width < 580:
            new_cols = 1
        elif canvas_width < 960:
            new_cols = 2
        else:
            new_cols = 3

        if new_cols != self.cols:
            self.cols = new_cols
            self._render_active_cards()

    def _render_active_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        cat = self.selected_category.get()
        buttons = TABS_DATA.get(cat, [])
        query = self.search_var.get().lower().strip()

        # Update canvas window width to match actual canvas width
        c_width = self.content_canvas.winfo_width()
        if c_width > 50:
            self.content_canvas.itemconfig(self.content_canvas_window, width=c_width)
            if c_width < 580:
                self.cols = 1
            elif c_width < 960:
                self.cols = 2
            else:
                self.cols = 3

        for c in range(self.cols):
            self.cards_frame.columnconfigure(c, weight=1, minsize=240)
        for c in range(self.cols, 8):
            self.cards_frame.columnconfigure(c, weight=0, minsize=0)

        visible_idx = 0
        self.all_button_cards.clear()

        start_row = 0
        if cat == "🏛️ SCHEMATIC VERİ SETİ (rom1504 Dataset)" and schematics_manager:
            try:
                studio_ui = schematics_manager.SchematicsStudioUI(
                    parent_cards_frame=self.cards_frame,
                    rcon_getter=lambda: self.rcon,
                    on_build_callback=lambda cmd: self.run_custom_template(cmd)
                )
                studio_ui.render()
                start_row = 1
            except Exception as e:
                self.log_console(f"Studio render error: {e}\n", tag="error")

        for btn_name, cmd_tmpl, desc in buttons:
            if query and (query not in btn_name.lower() and query not in desc.lower()):
                continue

            row = start_row + (visible_idx // self.cols)
            col = visible_idx % self.cols

            card = tk.Frame(
                self.cards_frame,
                bg=self.BG_CARD,
                highlightbackground=self.BORDER_COLOR,
                highlightthickness=1,
                padx=6,
                pady=4
            )
            card.grid(row=row, column=col, padx=4, pady=3, sticky="nsew")

            btn = tk.Button(
                card,
                text=btn_name,
                font=("Segoe UI", 8, "bold"),
                bg="#1e293b",
                fg=self.TEXT_COLOR,
                activebackground=self.ACCENT_CYAN,
                activeforeground="#000000",
                relief=tk.FLAT,
                anchor="w",
                padx=8,
                pady=2,
                command=lambda ct=cmd_tmpl: self.run_custom_template(ct)
            )
            btn.pack(fill=tk.X)

            desc_lbl = tk.Label(
                card,
                text=desc,
                font=("Segoe UI", 7),
                fg=self.TEXT_MUTED,
                bg=self.BG_CARD,
                anchor="w",
                justify="left"
            )
            desc_lbl.pack(fill=tk.X, padx=8, pady=(2, 0))

            self.all_button_cards.append((card, btn, btn_name, desc))
            visible_idx += 1

        if visible_idx == 0 and cat != "🏛️ SCHEMATIC VERİ SETİ (rom1504 Dataset)":
            msg_frame = tk.Frame(self.cards_frame, bg=self.BG_DARK, pady=30)
            msg_frame.grid(row=0, column=0, columnspan=self.cols, sticky="nsew")
            lbl_empty = tk.Label(
                msg_frame,
                text=f"🔍 Bu kategoride '{query}' ile eşleşen buton bulunamadı.",
                font=("Segoe UI", 9, "bold"),
                fg=self.ACCENT_GOLD,
                bg=self.BG_DARK
            )
            lbl_empty.pack(pady=4)
            btn_reset = tk.Button(
                msg_frame,
                text="❌ Aramayı Temizle ve Tümünü Göster",
                font=("Segoe UI", 8, "bold"),
                bg=self.ACCENT_CYAN,
                fg="#000000",
                relief=tk.FLAT,
                padx=8,
                pady=2,
                command=lambda: self.search_var.set("")
            )
            btn_reset.pack(pady=6)

        # Force Tkinter geometry update and refresh canvas scrollregion
        self.cards_frame.update_idletasks()
        bbox = self.content_canvas.bbox("all")
        if bbox:
            self.content_canvas.configure(scrollregion=bbox)
        self.content_canvas.yview_moveto(0.0)

    def _on_search_change(self, *args):
        self._render_active_cards()

    # =========================================================================
    # KONSOL & RCON BÖLÜMÜ
    # =========================================================================
    def _build_console_section(self):
        console_frame = tk.Frame(self.root, bg=self.BG_PANEL, height=145, padx=14, pady=4)
        console_frame.pack(fill=tk.X, side=tk.BOTTOM)

        top_bar = tk.Frame(console_frame, bg=self.BG_PANEL)
        top_bar.pack(fill=tk.X, pady=(0, 2))

        lbl = tk.Label(
            top_bar,
            text="💻 CANLI SUNUCU KONSOLU & GELİŞMİŞ CMD",
            font=("Segoe UI", 8, "bold"),
            fg=self.ACCENT_CYAN,
            bg=self.BG_PANEL
        )
        lbl.pack(side=tk.LEFT)

        btn_clear = tk.Button(
            top_bar,
            text="🧹 Konsolu Temizle",
            font=("Segoe UI", 7),
            bg=self.BG_CARD,
            fg=self.TEXT_MUTED,
            relief=tk.FLAT,
            padx=6,
            command=self._clear_console
        )
        btn_clear.pack(side=tk.RIGHT)

        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            height=4,
            bg="#030712",
            fg="#e2e8f0",
            insertbackground="#38bdf8",
            font=("Consolas", 8),
            relief=tk.FLAT
        )
        self.console_text.pack(fill=tk.X, pady=(0, 3))

        self.console_text.tag_config("cmd", foreground=self.ACCENT_CYAN, font=("Consolas", 8, "bold"))
        self.console_text.tag_config("info", foreground="#60a5fa")
        self.console_text.tag_config("warn", foreground="#fbbf24")
        self.console_text.tag_config("error", foreground="#f87171")
        self.console_text.tag_config("success", foreground=self.ACCENT_GREEN)

        cmd_bar = tk.Frame(console_frame, bg=self.BG_PANEL)
        cmd_bar.pack(fill=tk.X)

        cmd_lbl = tk.Label(cmd_bar, text="CMD >", font=("Consolas", 9, "bold"), fg=self.ACCENT_GREEN, bg=self.BG_PANEL)
        cmd_lbl.pack(side=tk.LEFT, padx=(0, 6))

        self.cmd_var = tk.StringVar()
        self.cmd_entry = tk.Entry(
            cmd_bar,
            textvariable=self.cmd_var,
            font=("Consolas", 9),
            bg=self.BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6), ipady=2)
        self.cmd_entry.bind("<Return>", lambda e: self.send_raw_command())
        self.cmd_entry.bind("<Up>", self._on_history_up)
        self.cmd_entry.bind("<Down>", self._on_history_down)

        btn_send = tk.Button(
            cmd_bar,
            text="Gönder (Enter)",
            font=("Segoe UI", 8, "bold"),
            bg=self.ACCENT_CYAN,
            fg="#000000",
            activebackground="#0284c7",
            relief=tk.FLAT,
            padx=14,
            command=self.send_raw_command
        )
        btn_send.pack(side=tk.RIGHT)

    def open_auto_server_maker(self):
        """Otomatik Sunucu Kurucu, AI Asistanı & Tünel Yöneticisini Başlatır"""
        try:
            builder_py = os.path.join(SERVER_DIR, "auto_server_maker.py")
            if os.path.exists(builder_py):
                subprocess.Popen([sys.executable, builder_py], cwd=SERVER_DIR)
                self.log_console("🚀 [Auto Server Maker & AI Hub] Yeni pencerede başlatıldı!\n", tag="success")
            else:
                messagebox.showerror("Hata", f"auto_server_maker.py bulunamadı:\n{builder_py}")
        except Exception as e:
            messagebox.showerror("Hata", f"Başlatılamadı: {e}")

    def show_hardware_metrics(self):
        """Shows live system telemetry in console"""
        try:
            from core.hardware_monitor import HardwareMonitor
            m = HardwareMonitor.get_system_metrics()
            msg = (
                f"\n📊 --- CANLI SİSTEM & DONANIM TELEMETRİSİ ---\n"
                f" İŞLEMCİ (CPU): %{m.get('cpu_percent', 0.0)}\n"
                f" BELLEK (RAM) : {m.get('ram_used_gb', 0)} GB / {m.get('ram_total_gb', 0)} GB (%{m.get('ram_percent', 0)})\n"
                f" BOŞ RAM      : {m.get('ram_free_gb', 0)} GB | BOŞ DİSK: {m.get('disk_free_gb', 0)} GB\n"
                f"----------------------------------------------\n"
            )
            self.log_console(msg, tag="success")
        except Exception as e:
            self.log_console(f"Donanım telemetrisi alınamadı: {e}\n", tag="error")

    def run_crash_doctor(self):
        """Analyzes latest.log or crash reports using local AI diagnostics"""
        self.log_console("🤖 [Crash Doctor] Sunucu logları ve çökme raporları taranıyor...\n", tag="cmd")
        def _worker():
            try:
                log_file = os.path.join(SERVER_DIR, "logs", "latest.log")
                content = ""
                if os.path.exists(log_file):
                    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                        lines = f.readlines()
                        content = "".join(lines[-150:])
                
                from core.ai_engineer import AIEngineer
                from core.config_manager import ConfigManager
                cfg = ConfigManager()
                ai = AIEngineer(cfg)
                prompt = (
                    "Aşağıdaki Minecraft Forge 1.20.1 sunucu loglarını incele. "
                    "Herhangi bir çakışma, hata, RAM yetersizliği veya çökme var mı? "
                    "Tespitlerini ve çözüm adımlarını net Türkçe olarak açıkla:\n\n" + (content or "Log dosyası temiz veya sunucu sorunsuz çalışıyor.")
                )
                diagnosis = ai.ask(prompt)
                self.root.after(0, self.log_console, f"\n🩺 [AI CRASH DOCTOR TEŞHİS RAPORU]:\n{diagnosis}\n\n", "success")
            except Exception as e:
                self.root.after(0, self.log_console, f"Crash Doctor hatası: {e}\n", "error")
        threading.Thread(target=_worker, daemon=True).start()

    def run_custom_template(self, cmd_template):
        if cmd_template == "__LAUNCH_AUTO_BUILDER__":
            self.open_auto_server_maker()
            return
        elif cmd_template == "__RUN_CRASH_DOCTOR__":
            self.run_crash_doctor()
            return
        elif cmd_template == "__SHOW_HARDWARE_METRICS__":
            self.show_hardware_metrics()
            return
        elif cmd_template == "__LAUNCH_PLAYIT_TUNNEL__":
            self.open_auto_server_maker()
            return

        target = self.player_var.get().strip() or "@p"
        qty = self.qty_var.get().strip() or "64"
        akce = getattr(self, "akce_var", None).get().strip() if getattr(self, "akce_var", None) else "50000"
        if not akce:
            akce = "50000"

        final_cmd = cmd_template.replace("{p}", target).replace("{qty}", qty).replace("{akce}", akce)
        self.log_console(f">> {final_cmd}\n", tag="cmd")
        threading.Thread(target=self._run_cmd_async, args=(final_cmd,), daemon=True).start()

    def assign_selected_role(self):
        target = self.player_var.get().strip() or "@p"
        role_label = self.role_var.get()
        if not target or role_label not in self.roles_dict:
            return
        team_name, prefix, title_text = self.roles_dict[role_label]
        cmd = f"team join {team_name} {target} && tab player {target} tabprefix {prefix} && tab player {target} tagprefix {prefix} && title {target} title {{\"text\":\"{title_text}\",\"color\":\"gold\",\"bold\":true}} && broadcast &8[&6Devlet&8] &e{target} &fartık resmi &6{role_label}&f makamına atandı! && playsound minecraft:ui.toast.challenge_complete master @a"
        self.log_console(f">> [Rol Atandı] {target} -> {role_label}\n", tag="success")
        threading.Thread(target=self._run_cmd_async, args=(cmd,), daemon=True).start()

    def send_raw_command(self):
        raw_cmd = self.cmd_var.get().strip()
        if not raw_cmd:
            return
        if raw_cmd.startswith("/"):
            raw_cmd = raw_cmd[1:]
        self.command_history.append(raw_cmd)
        self.history_index = len(self.command_history)
        self.cmd_var.set("")
        self.log_console(f">> {raw_cmd}\n", tag="cmd")
        threading.Thread(target=self._run_cmd_async, args=(raw_cmd,), daemon=True).start()

    def _run_cmd_async(self, cmd):
        sub_cmds = [c.strip() for c in cmd.split("&&") if c.strip()]
        for c in sub_cmds:
            if c.startswith("/"):
                c = c[1:]
            if c.startswith("give ") and ("{" in c or ":" in c):
                c = "minecraft:" + c
            resp = self.rcon.send_command(c)
            if resp:
                tag = "error" if ("Hata" in resp or "Bilinmeyen" in resp or "Error" in resp) else "success"
                self.log_console(f"{resp}\n", tag=tag)
            if len(sub_cmds) > 1:
                time.sleep(0.06)

    def log_console(self, text, tag="info"):
        self.console_text.insert(tk.END, text, tag)
        self.console_text.see(tk.END)

    def _clear_console(self):
        self.console_text.delete("1.0", tk.END)

    def _on_history_up(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.cmd_var.set(self.command_history[self.history_index])
        return "break"

    def _on_history_down(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.cmd_var.set(self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.cmd_var.set("")
        return "break"

    def start_server(self):
        self.log_console("[*] Sunucu baslatiliyor...\n", tag="cmd")
        bat_path = os.path.join(SERVER_DIR, "start.bat")
        threading.Thread(target=lambda: subprocess.Popen(["cmd.exe", "/c", "start", "", bat_path], cwd=SERVER_DIR), daemon=True).start()

    def stop_server(self):
        self.log_console("[*] Sunucu kapatma komutu gonderiliyor...\n", tag="cmd")
        bat_path = os.path.join(SERVER_DIR, "stop.bat")
        threading.Thread(target=lambda: subprocess.call([bat_path], cwd=SERVER_DIR), daemon=True).start()

    def _tail_log_thread(self):
        while self.running:
            if os.path.exists(LOG_FILE):
                try:
                    with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                        if self.log_pos == 0:
                            f.seek(0, os.SEEK_END)
                            self.log_pos = max(0, f.tell() - 2048)
                        f.seek(self.log_pos)
                        lines = f.readlines()
                        self.log_pos = f.tell()
                        for line in lines:
                            tag = "info"
                            if "WARN" in line:
                                tag = "warn"
                            elif "ERROR" in line or "Exception" in line:
                                tag = "error"
                            elif "joined the game" in line or "logged in with entity" in line:
                                tag = "success"
                                parts = line.split(" ")
                                for idx, p in enumerate(parts):
                                    if p == "joined" and idx > 0:
                                        pname = parts[idx-1].split("]")[-1].strip()
                                        if pname and pname not in self.player_entry['values']:
                                            vals = list(self.player_entry['values']) + [pname]
                                            self.player_entry['values'] = vals

                            # Otomatik Sohbet Yardım Asistanı (help / hlp / hewlp / yardım tespiti)
                            lower_line = line.lower()
                            if any(k in lower_line for k in ["help", "hlp", "hewlp", "yardim", "yardım", "komut"]):
                                m_sender = re.search(r'<([a-zA-Z0-9_]{3,16})>|\]\s*([a-zA-Z0-9_]{3,16})\s*:', line)
                                if m_sender:
                                    s_player = m_sender.group(1) or m_sender.group(2)
                                    if s_player and s_player.lower() not in ["rcon", "server", "console"]:
                                        threading.Thread(
                                            target=self.rcon.send_command,
                                            args=(f'tellraw {s_player} ["",{{"text":"💡 [REHBER] ","color":"gold","bold":true}},{{"text":"Tüm sunucu komutlarını görmek için ","color":"yellow"}},{{"text":"/help","color":"aqua","bold":true}},{{"text":" veya ","color":"yellow"}},{{"text":"/rehber","color":"green","bold":true}},{{"text":" yazabilirsiniz!","color":"yellow"}}]',),
                                            daemon=True
                                        ).start()
                            self.root.after(0, self.log_console, line, tag)
                except Exception:
                    pass
            time.sleep(1)

    def update_player_dropdown(self):
        """
        usercache.json ve aktif sunucudaki tüm oyuncuları (arkadaşlar, katılanlar) dinamik olarak çeker
        ve hedef açılır listesine ekler.
        """
        import json
        import re
        all_players = set()
        online_players = []

        # 1. usercache.json'dan kayıtlı tüm oyuncuları oku
        cache_file = os.path.join(SERVER_DIR, "usercache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data:
                        p_name = entry.get("name")
                        if p_name and re.match(r'^[a-zA-Z0-9_]{3,16}$', p_name):
                            all_players.add(p_name)
            except Exception:
                pass

        # 2. RCON üzerinden aktif oyuncuları sorgula
        try:
            res = self.rcon.send_command("minecraft:list")
            if not res or "online" not in res.lower():
                res = self.rcon.send_command("list")
            if res:
                words = re.findall(r'[a-zA-Z0-9_]{3,16}', res)
                ignore = {"there", "are", "players", "online", "max", "sunucuda", "aktif", "oyuncu", "cevrimici", "default", "kurucu", "oyuncular"}
                for w in words:
                    if w.lower() not in ignore:
                        all_players.add(w)
                        if w not in online_players:
                            online_players.append(w)
        except Exception:
            pass

        ordered_list = []
        for p in online_players:
            if p not in ordered_list:
                ordered_list.append(p)
        for p in sorted(all_players):
            if p not in ordered_list:
                ordered_list.append(p)
        for s in ["@a", "@p", "@r"]:
            if s not in ordered_list:
                ordered_list.append(s)

        if not ordered_list:
            ordered_list = ["Admin", "@a", "@p"]

        def _apply():
            curr = self.player_var.get().strip()
            self.player_entry.configure(values=ordered_list)
            if not curr:
                first_p = [x for x in ordered_list if not x.startswith("@")]
                if first_p:
                    self.player_var.set(first_p[0])

        self.root.after(0, _apply)

    def _status_monitor_thread(self):
        counter = 0
        while self.running:
            counter += 1
            is_online = False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.8)
                res = s.connect_ex(("127.0.0.1", 25565))
                s.close()
                is_online = (res == 0)
            except Exception:
                is_online = False

            if is_online:
                self.root.after(0, lambda: self.status_lbl.configure(text="● SUNUCU AKTİF (PORT 25565)", fg=self.ACCENT_GREEN, bg="#064e3b"))
                if counter % 3 == 0:
                    try:
                        self.update_player_dropdown()
                    except Exception:
                        pass
            else:
                self.root.after(0, lambda: self.status_lbl.configure(text="● SUNUCU KAPALI", fg=self.ACCENT_RED, bg="#450a0a"))
            time.sleep(3)

    def _autosave_worker(self):
        while self.running:
            for _ in range(180):
                if not self.running:
                    return
                time.sleep(1)
            if self.autosave_enabled:
                try:
                    res = self.rcon.send_command("save-all")
                    if res and ("Saved" in res or "Saving" in res or "OK" in res):
                        self.root.after(0, self.log_console, f"💾 [Oto-Kayıt] Dünya diske kaydedildi ({time.strftime('%H:%M:%S')})\n", "success")
                except Exception:
                    pass

    def _salary_worker(self):
        """Otomatik Maaş Dağıtıcısı: Her 10 dakikada bir tüm online oyunculara akçe verir"""
        while self.running:
            for _ in range(600):
                if not self.running:
                    return
                time.sleep(1)
            if self.salary_enabled.get():
                try:
                    amt = self.salary_amount.get().strip() or "250"
                    self.rcon.send_command(f"scoreboard players add @a akce {amt}")
                    self.rcon.send_command(f"eco give ** {amt}")
                    self.rcon.send_command(f'title @a actionbar {{"text":"💰 [MAAŞ]: Hesabınıza {amt} Akçe yatırıldı!","color":"gold","bold":true}}')
                    self.rcon.send_command("playsound minecraft:entity.experience_orb.pickup master @a")
                    self.root.after(0, self.log_console, f"💰 [Oto-Maaş]: Tüm oyunculara {amt} Akçe maaş dağıtıldı ({time.strftime('%H:%M:%S')})\n", "success")
                except Exception:
                    pass

    def _announcement_worker(self):
        """Periyodik Sunucu İpuçları & Duyuru Sistemi: Her 4 dakikada bir sunucuya yararlı ipucu atar"""
        hints = [
            'broadcast &8[&6Duyuru&8] &e/n &7veya &e/shop &ayazarak zengin Akçe marketinden eşya alıp satabilirsiniz!',
            'broadcast &8[&6Duyuru&8] &eAltın Kürek &aile iki köşeye sağ tıklayarak arsa kapatabilirsiniz. Arsanız patlamaz ve kırılmaz!',
            'broadcast &8[&6Duyuru&8] &e/takas <oyuncu> &ayazarak diğer oyuncularla güvenli takas yapabilirsiniz!',
            'broadcast &8[&6Duyuru&8] &e/kit baslangic &ave &e/kit gunluk &ayazarak ücretsiz hediyelerinizi almayı unutmayın!',
            'broadcast &8[&6Duyuru&8] &e/evkaydet <isim> &ave &e/ev <isim> &aile evinizi kaydedip dilediğiniz zaman ışınlanabilirsiniz!',
            'broadcast &8[&6Duyuru&8] &bTelefon, Tablet ve Konsol &foyuncuları da &e19132 &fportundan sunucuya bağlanabilir!'
        ]
        hint_idx = 0
        while self.running:
            for _ in range(240): # 4 dakika
                if not self.running:
                    return
                time.sleep(1)
            try:
                msg = hints[hint_idx % len(hints)]
                hint_idx += 1
                self.rcon.send_command(msg)
                self.rcon.send_command("playsound minecraft:block.note_block.chime master @a ~ ~ ~ 1 1")
            except Exception:
                pass

    def create_world_backup(self):
        """Tek tıkla dünya yedeğini backups klasörüne zip olarak kaydeder"""
        def _bg():
            self.log_console("💾 [*] Dünya yedeği alınıyor, lütfen bekleyin...\n", "cmd")
            try:
                import shutil, datetime
                backup_dir = os.path.join(SERVER_DIR, "backups")
                os.makedirs(backup_dir, exist_ok=True)
                ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                zip_name = f"world_backup_{ts}"
                zip_path = os.path.join(backup_dir, zip_name)
                world_dir = os.path.join(SERVER_DIR, "world")
                self.rcon.send_command("save-off")
                self.rcon.send_command("save-all flush")
                time.sleep(1)
                shutil.make_archive(zip_path, 'zip', world_dir)
                self.rcon.send_command("save-on")
                self.root.after(0, self.log_console, f"✅ [Yedek Başarılı]: {zip_name}.zip oluşturuldu! (backups klasöründe)\n", "success")
                messagebox.showinfo("Yedek Alındı", f"Dünya yedeği başarıyla alındı:\n{zip_name}.zip")
            except Exception as e:
                self.root.after(0, self.log_console, f"❌ [Yedek Hatası]: {str(e)}\n", "error")
                messagebox.showerror("Yedek Hatası", str(e))
        threading.Thread(target=_bg, daemon=True).start()

    def _lan_broadcast_worker(self):
        payload = b"[MOTD]\xc2\xa76\xc2\xa7lMinecraft Server \xc2\xa7f- \xc2\xa7aOnline[/MOTD][AD]25565[/AD]"
        while self.running:
            try:
                s_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_check.settimeout(0.5)
                res = s_check.connect_ex(("127.0.0.1", SERVER_PORT))
                s_check.close()
                if res == 0:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
                        sock.sendto(payload, ("224.0.2.60", 4445))
                        sock.sendto(payload, ("255.255.255.255", 4445))
                        sock.close()
                    except Exception:
                        pass
            except Exception:
                pass
            time.sleep(2.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGuiApp(root)
    root.mainloop()
