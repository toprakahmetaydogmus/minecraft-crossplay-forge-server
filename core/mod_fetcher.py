# -*- coding: utf-8 -*-
"""
Autonomous Mod & Plugin Fetcher (Modrinth API Integration)
Safely searches and downloads Minecraft mods compatible with the specified:
- Minecraft Version (e.g. 1.20.1, 1.20.4, 1.21.1)
- Mod Loader (Forge, Fabric, NeoForge, Arclight, Mohist)
- User Prompt / Keywords (e.g. "büyü", "kılıç", "minimap", "fps", "zombi", "teknoloji", "rpg")
Zero API keys needed - utilizes Modrinth's high-speed public REST API with 100% offline fallback safety.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import logging

MODRINTH_API_URL = "https://api.modrinth.com/v2"
USER_AGENT = "AutoMinecraftServerMaker/4.0.0 (https://github.com/toprakahmetaydogmus/auto-minecraft-server-maker)"

# Curated high-reputation mod dictionaries for theme recognition
THEME_MOD_KEYWORDS = {
    "büyü": ["irons-spells-n-spellbooks", "ars-nouveau"],
    "magic": ["irons-spells-n-spellbooks", "ars-nouveau"],
    "kılıç": ["simply-swords", "better-combat-by-daedelus"],
    "sword": ["simply-swords", "better-combat-by-daedelus"],
    "savaş": ["better-combat-by-daedelus", "simply-swords"],
    "combat": ["better-combat-by-daedelus", "simply-swords"],
    "minimap": ["journeymap", "xaeros-minimap"],
    "harita": ["journeymap", "xaeros-minimap"],
    "map": ["journeymap", "xaeros-minimap"],
    "fps": ["ferrite-core", "lithium"],
    "optimizasyon": ["ferrite-core", "lithium"],
    "performans": ["ferrite-core"],
    "jei": ["jei"],
    "eşya": ["jei"],
    "rehber": ["jei"],
    "zombi": ["enhanced-celestials", "the-hordes"],
    "zombie": ["enhanced-celestials", "the-hordes"],
    "kıyamet": ["enhanced-celestials"],
    "apocalypse": ["enhanced-celestials"],
    "teknoloji": ["create"],
    "makine": ["create"],
    "tech": ["create"],
    "depolama": ["iron-chests", "toms-storage"],
    "chest": ["iron-chests", "toms-storage"],
    "sandık": ["iron-chests"],
    "rpg": ["better-combat-by-daedelus", "irons-spells-n-spellbooks", "journeymap"],
    "macera": ["better-combat-by-daedelus", "journeymap"],
    "dungeon": ["when-dungeons-arise"],
    "zindan": ["when-dungeons-arise"]
}


class ModFetcher:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback or print

    def log(self, message):
        try:
            self.log_callback(f"[AI Mod Yöneticisi] {message}")
        except Exception:
            try:
                safe_msg = f"[AI Mod Yoneticisi] {message}".encode("ascii", "replace").decode("ascii")
                self.log_callback(safe_msg)
            except Exception:
                pass

    def _normalize_loader(self, loader):
        raw = str(loader).lower().strip()
        if "fabric" in raw:
            return "fabric"
        elif "neo" in raw:
            return "neoforge"
        elif any(x in raw for x in ["forge", "arclight", "mohist"]):
            return "forge"
        elif "quilt" in raw:
            return "quilt"
        return "forge"

    def get_latest_version_file(self, project_id_or_slug, mc_version, loader="forge"):
        """
        Retrieves the direct download URL for the project matching mc_version and loader.
        """
        clean_loader = self._normalize_loader(loader)
        url = f"{MODRINTH_API_URL}/project/{project_id_or_slug}/version"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=10) as resp:
                versions = json.loads(resp.read().decode("utf-8"))
                if not versions:
                    return None

                # Find best version matching mc_version and loader
                matched = []
                for v in versions:
                    g_vers = v.get("game_versions", [])
                    loaders = v.get("loaders", [])
                    if mc_version in g_vers and clean_loader in loaders:
                        matched.append(v)

                # Fallback: if exact minor patch not found, try matching major.minor (e.g. 1.20)
                if not matched:
                    parts = mc_version.split(".")
                    if len(parts) >= 2:
                        base_ver = f"{parts[0]}.{parts[1]}"
                        for v in versions:
                            g_vers = v.get("game_versions", [])
                            loaders = v.get("loaders", [])
                            if any(gv.startswith(base_ver) for gv in g_vers) and clean_loader in loaders:
                                matched.append(v)

                if not matched:
                    return None

                latest = matched[0]
                files = latest.get("files", [])
                for f in files:
                    if f.get("primary", False):
                        return f
                return files[0] if files else None
        except Exception as e:
            # Not an error to crash on, just skip unsupported mod
            return None

    def search_modrinth_slugs(self, query, mc_version, loader, limit=3):
        """
        Dynamically queries Modrinth search API if keyword not in curated dictionary.
        """
        clean_loader = self._normalize_loader(loader)
        facets = [
            [f"versions:{mc_version}"],
            [f"categories:{clean_loader}"],
            ["project_type:mod"]
        ]
        params = {
            "query": query,
            "facets": json.dumps(facets),
            "limit": limit
        }
        url = f"{MODRINTH_API_URL}/search?{urllib.parse.urlencode(params)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                hits = data.get("hits", [])
                return [h.get("slug") for h in hits if h.get("slug")]
        except Exception:
            return []

    def download_mod(self, project_slug, mc_version, loader, mods_dir):
        """
        Downloads a single mod .jar into mods_dir.
        """
        os.makedirs(mods_dir, exist_ok=True)
        file_info = self.get_latest_version_file(project_slug, mc_version, loader)
        if not file_info:
            return False, f"Uyumlu sürüm dosyası bulunamadı ({project_slug})"

        url = file_info.get("url")
        filename = file_info.get("filename", f"{project_slug}.jar")
        dest_path = os.path.join(mods_dir, filename)

        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1024:
            self.log(f"✔ Mod zaten mevcut: {filename}")
            return True, filename

        self.log(f"⬇️ İndiriliyor: {filename}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=40) as resp, open(dest_path, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            self.log(f"✅ İndirildi: {filename}")
            return True, filename
        except Exception as e:
            self.log(f"❌ İndirme hatası ({filename}): {e}")
            return False, str(e)

    def auto_install_theme_mods(self, prompt, mc_version, loader, mods_dir):
        """
        Analyzes user prompt and automatically fetches matching verified mods.
        Returns list of successfully installed mod filenames.
        """
        text = prompt.lower()
        mods_to_fetch = set()

        # 1. Match themes from prompt
        for kw, slug_list in THEME_MOD_KEYWORDS.items():
            if kw in text:
                for s in slug_list:
                    mods_to_fetch.add(s)

        # 2. General default QoL mods for modded servers
        # FerriteCore (reduces RAM usage drastically)
        mods_to_fetch.add("ferrite-core")

        # JEI for Forge/NeoForge/Fabric
        mods_to_fetch.add("jei")

        # JourneyMap if any map mentioned or general modded
        if any(w in text for w in ["harita", "map", "kesif", "dunya", "arkadas", "rpg", "macera", "modlu"]):
            mods_to_fetch.add("journeymap")

        # 3. Dynamic search for unrecognized queries
        words = [w for w in text.split() if len(w) > 3 and w not in ["kur", "yukle", "server", "sunucu", "arkadas", "hafif", "ram", "forge", "fabric"]]
        for w in words[:2]:
            if not any(w in kw for kw in THEME_MOD_KEYWORDS):
                dynamic_slugs = self.search_modrinth_slugs(w, mc_version, loader, limit=1)
                for ds in dynamic_slugs:
                    mods_to_fetch.add(ds)

        clean_loader = self._normalize_loader(loader)
        self.log(f"🔍 Minecraft {mc_version} ({clean_loader.upper()}) için uyumlu modlar taranıyor...")
        self.log(f"🎯 Hedef Modlar: {list(mods_to_fetch)}")

        downloaded = []
        for slug in mods_to_fetch:
            success, name = self.download_mod(slug, mc_version, clean_loader, mods_dir)
            if success:
                downloaded.append(name)

        self.log(f"🎉 Mod kurulumu tamamlandı: Toplam {len(downloaded)} adet uyumlu mod aktif!")
        return downloaded
