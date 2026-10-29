# -*- coding: utf-8 -*-
"""
1-Click Plugin & Mod Hub (v3.9.0 Ultimate)
Autonomous downloader & installer for essential high-performance Minecraft plugins.
Direct download from official verified CDNs and repositories.
"""

import os
import urllib.request
import threading
import logging

POPULAR_PLUGINS = [
    {
        "id": "geyser",
        "name": "Geyser-Spigot",
        "category": "Crossplay",
        "desc": "Bedrock (Mobil & Konsol) oyuncularının Java sunucusuna bağlanmasını sağlar.",
        "url": "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
        "filename": "Geyser-Spigot.jar"
    },
    {
        "id": "floodgate",
        "name": "Floodgate",
        "category": "Crossplay",
        "desc": "Bedrock oyuncularının Java hesabı olmadan kolayca giriş yapmasını sağlar.",
        "url": "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
        "filename": "floodgate-spigot.jar"
    },
    {
        "id": "viaversion",
        "name": "ViaVersion",
        "category": "Uyumluluk",
        "desc": "Daha yeni Minecraft sürümlerinin eski sunuculara girmesini sağlar.",
        "url": "https://api.spiget.org/v2/resources/19254/download",
        "filename": "ViaVersion.jar"
    },
    {
        "id": "viabackwards",
        "name": "ViaBackwards",
        "category": "Uyumluluk",
        "desc": "Daha eski Minecraft istemcilerinin yeni sunuculara girmesini sağlar.",
        "url": "https://api.spiget.org/v2/resources/27448/download",
        "filename": "ViaBackwards.jar"
    },
    {
        "id": "essentialsx",
        "name": "EssentialsX",
        "category": "Yönetim",
        "desc": "Temel sunucu komutları: /sethome, /spawn, /warp, /tpa, /fly vb.",
        "url": "https://api.spiget.org/v2/resources/9089/download",
        "filename": "EssentialsX.jar"
    },
    {
        "id": "luckperms",
        "name": "LuckPerms",
        "category": "Yetki & Rütbe",
        "desc": "Minecraft'ın en gelişmiş, modern web editörlü yetki ve rütbe yönetim eklentisi.",
        "url": "https://download.luckperms.net/1559/bukkit/loader/LuckPerms-Bukkit-5.4.145.jar",
        "filename": "LuckPerms.jar"
    },
    {
        "id": "vault",
        "name": "Vault",
        "category": "Ekonomi & API",
        "desc": "Tüm ekonomi ve yetki eklentilerinin birbiriyle konuşmasını sağlayan temel köprü.",
        "url": "https://api.spiget.org/v2/resources/34315/download",
        "filename": "Vault.jar"
    },
    {
        "id": "worldedit",
        "name": "WorldEdit",
        "category": "İnşa & Yapı",
        "desc": "Büyük yapıları saniyeler içinde inşa etme ve harita düzenleme aracı.",
        "url": "https://mediafilez.forgecdn.net/files/5460/346/worldedit-bukkit-7.3.6.jar",
        "filename": "WorldEdit.jar"
    },
    {
        "id": "chunky",
        "name": "Chunky",
        "category": "Lag Önleme",
        "desc": "Dünya chunk'larını önceden oluşturarak oyuncular gezerken oluşan lagı %95 yok eder.",
        "url": "https://api.spiget.org/v2/resources/81534/download",
        "filename": "Chunky.jar"
    },
    {
        "id": "clearlag",
        "name": "ClearLag",
        "category": "Lag Önleme",
        "desc": "Yerdeki gereksiz eşyaları ve fazla entity'leri otomatik temizler, RAM kazandırır.",
        "url": "https://api.spiget.org/v2/resources/28271/download",
        "filename": "ClearLag.jar"
    },
    {
        "id": "skinsrestorer",
        "name": "SkinsRestorer",
        "category": "Görsel",
        "desc": "Tüm oyuncuların gerçek Minecraft skinlerini eksiksiz gösterir (/skin komutu).",
        "url": "https://api.spiget.org/v2/resources/2124/download",
        "filename": "SkinsRestorer.jar"
    },
    {
        "id": "authme",
        "name": "AuthMe Reloaded",
        "category": "Güvenlik & Giriş",
        "desc": "Korsan/ücretsiz sunucularda oyuncuların hesaplarını şifreyle korur (/register, /login).",
        "url": "https://api.spiget.org/v2/resources/6269/download",
        "filename": "AuthMe-Reloaded.jar"
    },
    {
        "id": "spark",
        "name": "Spark Profiler",
        "category": "Analiz & TPS",
        "desc": "Sunucudaki lagın hangi mod, plugin veya chunk'tan kaynaklandığını tespit eder.",
        "url": "https://sparkapi.lucko.me/download/bukkit",
        "filename": "spark.jar"
    },
    {
        "id": "griefprevention",
        "name": "GriefPrevention",
        "category": "Koruma & Claim",
        "desc": "Oyuncuların altın kürekle arazi sahiplenmesini sağlayarak sandık ve ev hırsızlığını engeller.",
        "url": "https://api.spiget.org/v2/resources/1884/download",
        "filename": "GriefPrevention.jar"
    },
    {
        "id": "multiverse",
        "name": "Multiverse-Core",
        "category": "Çoklu Dünya",
        "desc": "Birden çok dünya yönetimi (Ayrı Survival dünyası, Maden dünyası, Skyblock dünyası).",
        "url": "https://api.spiget.org/v2/resources/390/download",
        "filename": "Multiverse-Core.jar"
    }
]

class PluginModHub:
    def __init__(self, target_dir, log_callback=None):
        self.target_dir = os.path.abspath(target_dir)
        self.plugins_dir = os.path.join(self.target_dir, "plugins")
        self.log_callback = log_callback or print

    def log(self, msg):
        try:
            self.log_callback(f"[Plugin Hub] {msg}")
        except Exception:
            pass

    def get_installed_plugins(self):
        """Lists all installed jar files in plugins directory."""
        if not os.path.exists(self.plugins_dir):
            return []
        return [f for f in os.listdir(self.plugins_dir) if f.lower().endswith(".jar")]

    def is_plugin_installed(self, filename):
        return os.path.exists(os.path.join(self.plugins_dir, filename))

    def install_plugin(self, plugin_info, progress_callback=None):
        """Downloads and installs a plugin into the server's plugins directory."""
        os.makedirs(self.plugins_dir, exist_ok=True)
        dest_path = os.path.join(self.plugins_dir, plugin_info["filename"])
        url = plugin_info["url"]

        self.log(f"'{plugin_info['name']}' indiriliyor...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoMinecraftServerMaker/3.9.0"})
            with urllib.request.urlopen(req, timeout=45) as resp, open(dest_path, "wb") as out:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    out.write(chunk)
                    downloaded += len(chunk)
                    if total > 0 and progress_callback:
                        pct = int((downloaded / total) * 100)
                        progress_callback(pct, f"%{pct} indirildi")

            self.log(f"✅ '{plugin_info['name']}' başarıyla plugins klasörüne kuruldu!")
            return True
        except Exception as e:
            self.log(f"❌ '{plugin_info['name']}' indirme hatası: {e}")
            return False
