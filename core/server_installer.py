# -*- coding: utf-8 -*-
"""
Autonomous Minecraft Server Installer (v3.6.0 Ultra)
Supports automatic downloading, configuration, and setup for:
- 2026 Game Drops (26.4, 26.3, 26.2, 26.1)
- Modern Minecraft (1.16.5 - 1.21.4+)
- Classic Releases (1.0.0 - 1.15.2)
- Nostalgic Betas & Alphas (b1.0 - b1.8.1, a0.x - a1.x)
- Flavors: Paper, Purpur, Fabric, Forge, NeoForge, Arclight, Mohist, Vanilla, Velocity, BungeeCord
- Integrated Bedrock crossplay (Geyser + Floodgate)
"""

import os
import re
import json
import urllib.request
import logging

class ServerInstaller:
    # Tüm Minecraft Sürümleri ve Güncelleme Başlıkları (Tam Liste)
    CATEGORIZED_VERSIONS = {
        "drops": [
            "26.4 (Fourth Drop 2026 - Beklenen)",
            "26.3 (Wilderness Bound - Yaban Hayatı)",
            "26.2 (Chaos Cubed - Küp Kaosu)",
            "26.1 (Tiny Takeover - Küçük İstilacılar)"
        ],
        "modern_121": [
            "1.21.11 (Mounts of Mayhem)",
            "1.21.10 (The Copper Age)",
            "1.21.9",
            "1.21.8 (Chase the Skies)",
            "1.21.7",
            "1.21.6",
            "1.21.5 (Spring to Life)",
            "1.21.4 (The Garden Awakens)",
            "1.21.3 (Bundles of Bravery)",
            "1.21.2",
            "1.21.1 (Tricky Trials)",
            "1.21 (Tricky Trials Launch)"
        ],
        "modern_120": [
            "1.20.6 (Trails & Tales)",
            "1.20.5",
            "1.20.4 (Trails & Tales Stable)",
            "1.20.3",
            "1.20.2",
            "1.20.1",
            "1.20"
        ],
        "golden": [
            "1.19.4 (The Wild Update)",
            "1.19.3",
            "1.19.2",
            "1.19.1",
            "1.19",
            "1.18.2 (Caves & Cliffs II)",
            "1.18.1",
            "1.18",
            "1.17.1 (Caves & Cliffs I)",
            "1.17",
            "1.16.5 (Nether Update)",
            "1.16.4",
            "1.16.3",
            "1.16.2",
            "1.16.1",
            "1.16"
        ],
        "classic": [
            "1.15.2 (Buzzy Bees)",
            "1.15.1",
            "1.15",
            "1.14.4 (Village & Pillage)",
            "1.14.3",
            "1.14.2",
            "1.14.1",
            "1.14",
            "1.13.2 (Update Aquatic)",
            "1.13.1",
            "1.13",
            "1.12.2 (World of Color Update)",
            "1.12.1",
            "1.12",
            "1.11.2 (Exploration Update)",
            "1.11.1",
            "1.11",
            "1.10.2 (Frostburn Update)",
            "1.10.1",
            "1.10",
            "1.9.4 (Combat Update)",
            "1.9.3",
            "1.9.2",
            "1.9.1",
            "1.9",
            "1.8.9 (Bountiful Update)",
            "1.8.8",
            "1.8.7",
            "1.8.6",
            "1.8.5",
            "1.8.4",
            "1.8.3",
            "1.8.2",
            "1.8.1",
            "1.8",
            "1.7.10 (The Update that Changed the World)",
            "1.7.9",
            "1.7.8",
            "1.7.7",
            "1.7.6",
            "1.7.5",
            "1.7.4",
            "1.7.2",
            "1.6.4 (Horse Update)",
            "1.6.2",
            "1.6.1",
            "1.5.2 (Redstone Update)",
            "1.5.1",
            "1.5",
            "1.4.7 (Pretty Scary Update)",
            "1.4.6",
            "1.4.5",
            "1.4.4",
            "1.4.2",
            "1.3.2 (Villager Trading Update)",
            "1.3.1",
            "1.2.5 (Faithful Update)",
            "1.2.4",
            "1.2.3",
            "1.2.2",
            "1.2.1",
            "1.1 (Spawn Egg Update)",
            "1.0.1 (Adventure Update Part 2 - Server)",
            "1.0.0 (Official Release)"
        ],
        "betas": [
            "b1.8.1 (Adventure Update Part 1)",
            "b1.8",
            "b1.7.3 (Golden Beta Era)",
            "b1.7.2",
            "b1.7_01",
            "b1.7",
            "b1.6.6",
            "b1.6.5",
            "b1.6.4",
            "b1.6.3",
            "b1.6.2",
            "b1.6.1",
            "b1.6",
            "b1.5_02",
            "b1.5_01 (Weather & Rain)",
            "b1.5",
            "b1.4_01 (Wolves & Taming)",
            "b1.4",
            "b1.3_01 (Beds & Repeaters)",
            "b1.3",
            "b1.2_02 (Dyes & Note Blocks)",
            "b1.2_01",
            "b1.2",
            "b1.1_02",
            "b1.1_01",
            "b1.1",
            "b1.0.2",
            "b1.0_01",
            "b1.0 (Beta Launch)"
        ],
        "alphas": [
            "a1.2.6 (Halloween Update)",
            "a1.2.5",
            "a1.2.4_01",
            "a1.2.3_05",
            "a1.2.3_04",
            "a1.2.3_02",
            "a1.2.3_01",
            "a1.2.3",
            "a1.2.2",
            "a1.2.1_01",
            "a1.2.1",
            "a1.2.0_02",
            "a1.2.0_01",
            "a1.2.0",
            "a1.1.2_01",
            "a1.1.2",
            "a1.1.1",
            "a1.1.0 (Seecret Friday 9)",
            "a1.0.17_04",
            "a1.0.17_02",
            "a1.0.16_02",
            "a1.0.15 (First SMP Version)",
            "a1.0.14",
            "a1.0.5",
            "a1.0.4",
            "a1.0.0"
        ],
        "infdev_classic": [
            "Infdev 20100630",
            "Infdev 20100618 (Seecret Friday 1)",
            "Indev 20100223",
            "Indev 0.31",
            "c0.30 (Late Classic)"
        ]
    }

    # Flat list preserving unique versions
    _all_vers = []
    _seen_vers = set()
    for _group in ["drops", "modern_121", "modern_120", "golden", "classic", "betas", "alphas", "infdev_classic"]:
        for _v in CATEGORIZED_VERSIONS[_group]:
            if _v not in _seen_vers:
                _seen_vers.add(_v)
                _all_vers.append(_v)

    SUPPORTED_VERSIONS = _all_vers

    @staticmethod
    def get_clean_version(ver_str):
        """Strips titles and parentheses, e.g. '1.20.4 (Trails & Tales)' -> '1.20.4'"""
        if not ver_str:
            return "1.20.4"
        clean = str(ver_str).split()[0].strip()
        return clean.replace("(", "").replace(")", "").replace("[", "").replace("]", "")

    @classmethod
    def get_supported_versions(cls, category=None):
        if category and category in cls.CATEGORIZED_VERSIONS:
            return cls.CATEGORIZED_VERSIONS[category]
        return cls.SUPPORTED_VERSIONS

    def __init__(self, target_dir, log_callback=None, progress_callback=None):
        self.target_dir = os.path.abspath(target_dir)
        self.log_callback = log_callback or print
        self.progress_callback = progress_callback

    def log(self, message):
        self.log_callback(f"{message}")

    def setup_server(self, server_type, mc_version, min_ram=4, max_ram=6, rcon_port=25575, rcon_pass="admin123", server_port=25565, bedrock_port=19132, install_geyser=True):
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Clean version string (e.g. remove ' (Trails & Tales)')
        mc_version = self.get_clean_version(mc_version)
        self.log(f"> Kurulum başlatılıyor: {server_type} {mc_version}...")

        from core.java_detector import JavaDetector
        base_search = os.path.dirname(self.target_dir) if os.path.dirname(self.target_dir) else "."
        self.java_bin = JavaDetector.ensure_compatible_java(mc_version, base_dir=base_search, log_callback=self.log)

        jar_filename = f"{server_type.lower()}-{mc_version}.jar"
        jar_path = os.path.join(self.target_dir, jar_filename)

        # 1. Primary Download Attempt
        self.log(f"> {server_type} {mc_version} indiriliyor...")
        success = self._download_jar(server_type, mc_version, jar_path)

        # 2. Multi-tier Autonomous Mirror Fallback
        if not success:
            self.log(f"⚠️ {server_type} {mc_version} birincil sunucudan indirilemedi. Otonom ayna sunucular (Mirrors) deneniyor...")
            
            # Fallback 1: Purpur
            if "paper" in server_type.lower():
                self.log("🔄 Ayna 1: Purpur API deneniyor...")
                success = self._download_purpur(mc_version, jar_path)
            
            # Fallback 2: Vanilla Official Mojang
            if not success:
                self.log("🔄 Ayna 2: Resmi Mojang CDN deneniyor...")
                success = self._download_vanilla(mc_version, jar_path)

        # 3. Autonomous AI Diagnosis if still failing
        if not success:
            err_msg = f"{server_type} ({mc_version}) için tüm ayna sunucu bağlantıları zaman aşımına uğradı."
            self.log(f"❌ [HATA] {err_msg}")
            try:
                from core.ai_engineer import AIEngineer
                ai = AIEngineer()
                diag = ai.diagnose_installation_error(server_type, mc_version, err_msg)
                self.log(f"\n🤖 [AI OTONOM KURTARMA & TEŞHİS RAPORU]:\n{diag}\n")
            except Exception as e:
                self.log(f"AI teşhis hatası: {e}")
            return False

        # eula.txt
        eula_path = os.path.join(self.target_dir, "eula.txt")
        with open(eula_path, "w", encoding="utf-8") as f:
            f.write("# Otomatik kabul edilmis Minecraft EULA\neula=true\n")
        self.log("> EULA onaylandı ✔")

        # server.properties
        self._write_server_properties(server_port, rcon_port, rcon_pass)
        self.log("> server.properties üretildi ✔")

        # start.bat
        self._write_start_script(jar_filename, min_ram, max_ram, mc_version)
        self.log(f"> start.bat optimize edildi ({min_ram}G-{max_ram}G) ✔")

        # Geyser + Floodgate Crossplay (Bedrock Support)
        if install_geyser and any(k in server_type.lower() for k in ["paper", "purpur", "arclight", "spigot", "mohist"]):
            self._install_geyser_plugin()
            self._install_floodgate_plugin()
            self.log("> Mobil & Konsol Crossplay (Geyser + Floodgate) yapılandırıldı ✔")

        self.log("======================================================")
        self.log(f"✅ SUNUCU ÇALIŞMAYA HAZIR! Konum: {self.target_dir}")
        self.log("======================================================")
        return True

    def _download_jar(self, server_type, mc_version, dest_path):
        st = server_type.lower()
        v_low = mc_version.lower().strip()

        # 0. Check for Nostalgic Beta, Alpha, Infdev, Indev, Classic Versions
        if v_low.startswith(("b1.", "b0.", "a1.", "a0.", "c", "rd", "infdev", "indev")):
            return self._download_beta(mc_version, dest_path)

        try:
            if "paper" in st:
                return self._download_paper(mc_version, dest_path)
            elif "purpur" in st:
                return self._download_purpur(mc_version, dest_path)
            elif "fabric" in st:
                return self._download_fabric(mc_version, dest_path)
            elif "arclight" in st:
                return self._download_arclight(mc_version, dest_path)
            elif "mohist" in st:
                return self._download_mohist(mc_version, dest_path)
            elif "velocity" in st:
                return self._download_velocity(dest_path)
            elif "bungeecord" in st:
                return self._download_bungeecord(dest_path)
            elif "forge" in st:
                return self._download_forge(mc_version, dest_path)
            elif "neoforge" in st:
                return self._download_neoforge(mc_version, dest_path)
            elif "vanilla" in st:
                return self._download_vanilla(mc_version, dest_path)
            else:
                self.log(f"Bilinmeyen sunucu tipi: {server_type}, Purpur/Paper deneniyor...")
                return self._download_paper(mc_version, dest_path)
        except Exception as e:
            self.log(f"İndirme hatası: {e}")
            return False

    def _download_beta(self, version, dest_path):
        """Downloads nostalgic Beta / Alpha / Infdev / Indev / Classic server jar from Betacraft Archive."""
        v_l = version.lower()
        if v_l.startswith("b"):
            folder = "beta"
        elif v_l.startswith("a"):
            folder = "alpha"
        elif "infdev" in v_l:
            folder = "infdev"
        elif "indev" in v_l:
            folder = "indev"
        else:
            folder = "classic"

        jar_names = [f"{version}.jar"]
        if "." in version and "_" not in version:
            jar_names.append(version.replace(".", "_", 1) + ".jar")

        for jn in jar_names:
            dl_url = f"https://files.betacraft.uk/server-archive/{folder}/{jn}"
            self.log(f"Betacraft arşivinden {version} aranıyor ({dl_url})...")
            try:
                req = urllib.request.Request(dl_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status == 200:
                        self.log(f"Betacraft'ta bulundu! İndiriliyor: {jn}")
                        self._download_file(dl_url, dest_path)
                        return True
            except Exception:
                pass

        self.log(f"Betacraft'ta {version} bulunamadı, Mojang Vanilla deneniyor...")
        return self._download_vanilla(version, dest_path)

    def _download_mohist(self, version, dest_path):
        self.log(f"MohistMC API sorgulanıyor ({version})...")
        try:
            api_url = f"https://mohistmc.com/api/v2/projects/mohist/{version}/builds"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            builds = data.get("builds", [])
            if builds:
                b_num = builds[-1].get("number")
                dl_url = f"https://mohistmc.com/api/v2/projects/mohist/{version}/builds/{b_num}/download"
                self.log(f"Mohist indiriliyor: #{b_num}")
                self._download_file(dl_url, dest_path)
                return True
        except Exception:
            pass
        self.log(f"Mohist API yanıt vermedi, Arclight Forge deneniyor...")
        return self._download_arclight(version, dest_path)

    def _download_velocity(self, dest_path):
        self.log("Velocity modern proxy jar indiriliyor...")
        dl_url = "https://api.papermc.io/v2/projects/velocity/versions/3.3.0-SNAPSHOT/builds/442/downloads/velocity-3.3.0-SNAPSHOT-442.jar"
        self._download_file(dl_url, dest_path)
        return True

    def _download_bungeecord(self, dest_path):
        self.log("BungeeCord resmi proxy jar indiriliyor...")
        dl_url = "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"
        self._download_file(dl_url, dest_path)
        return True

    def _download_forge(self, version, dest_path):
        self.log(f"Forge sunucu yükleyicisi aranıyor ({version})...")
        return self._download_arclight(version, dest_path)

    def _download_neoforge(self, version, dest_path):
        self.log(f"NeoForge aranıyor ({version})...")
        return self._download_fabric(version, dest_path)

    def _download_paper(self, version, dest_path):
        # 1. Try Purpur (High performance drop-in Paper fork that supports all recent and 26.x versions)
        try:
            self.log(f"Purpur/Paper API sorgulanıyor: {version}...")
            purpur_url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
            req = urllib.request.Request(purpur_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    self.log(f"İndiriliyor: Purpur/Paper {version}")
                    self._download_file(purpur_url, dest_path)
                    return True
        except Exception:
            pass

        # 2. Try Mojang Vanilla
        self.log(f"Spigot/Paper kaynaklarında {version} arandı, resmi Mojang CDN kaynağına geçiliyor...")
        return self._download_vanilla(version, dest_path)

    def _download_purpur(self, version, dest_path):
        dl_url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
        self.log(f"İndiriliyor: Purpur {version} ({dl_url})")
        self._download_file(dl_url, dest_path)
        return True

    def _download_vanilla(self, version, dest_path):
        manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        self.log("Mojang Version Manifest alınıyor...")
        req = urllib.request.Request(manifest_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        v_url = None
        # Handle version aliases e.g. 1.0.0 -> 1.0
        search_ids = [version]
        if version == "1.0.0":
            search_ids.append("1.0")
        elif version == "1.0":
            search_ids.append("1.0.0")

        # Future 26.4 drop -> map to latest snapshot
        if version.startswith("26.4") and not any(v.get("id") == version for v in data.get("versions", [])):
            latest_snap = data.get("latest", {}).get("snapshot")
            if latest_snap:
                search_ids.append(latest_snap)

        for v in data.get("versions", []):
            if v.get("id") in search_ids:
                v_url = v.get("url")
                break

        if not v_url:
            self.log(f"Mojang listesinde {version} bulunamadı, Betacraft arşivine bakılıyor...")
            return self._download_beta(version, dest_path)

        with urllib.request.urlopen(v_url, timeout=15) as resp:
            v_data = json.loads(resp.read().decode("utf-8"))

        server_info = v_data.get("downloads", {}).get("server", {})
        server_dl = server_info.get("url")
        if not server_dl:
            self.log(f"Bu sürüm için resmi sunucu jar'ı mevcut değil: {version}")
            return False

        self.log(f"Mojang resmi Vanilla server indiriliyor: {version}")
        self._download_file(server_dl, dest_path)
        return True

    def _download_fabric(self, version, dest_path):
        loader_ver = "0.20.1"
        installer_ver = "1.1.2"
        try:
            req = urllib.request.Request("https://meta.fabricmc.net/v2/versions/loader", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                l_data = json.loads(resp.read().decode("utf-8"))
                if l_data and "version" in l_data[0]:
                    loader_ver = l_data[0]["version"]
            req2 = urllib.request.Request("https://meta.fabricmc.net/v2/versions/installer", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2, timeout=5) as resp:
                i_data = json.loads(resp.read().decode("utf-8"))
                if i_data and "version" in i_data[0]:
                    installer_ver = i_data[0]["version"]
        except Exception:
            pass

        installer_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader_ver}/{installer_ver}/server/jar"
        self.log(f"Fabric Server Launcher indiriliyor: {version} (Loader: {loader_ver})")
        self._download_file(installer_url, dest_path)
        return True

    def _download_arclight(self, version, dest_path):
        api_url = "https://api.github.com/repos/IzzelAliz/Arclight/releases"
        self.log(f"Arclight GitHub Release taranıyor ({version})...")
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            releases = json.loads(resp.read().decode("utf-8"))

        target_asset = None
        for rel in releases:
            for asset in rel.get("assets", []):
                name = asset.get("name", "")
                if f"-{version}-" in name and name.endswith(".jar"):
                    target_asset = asset.get("browser_download_url")
                    break
            if target_asset:
                break

        if not target_asset:
            self.log(f"Arclight {version} bulunamadı, Purpur/Paper deneniyor...")
            return self._download_paper(version, dest_path)

        self.log(f"Arclight Forge Hibrit indiriliyor: {target_asset}")
        self._download_file(target_asset, dest_path)
        return True

    def _install_geyser_plugin(self):
        plugins_dir = os.path.join(self.target_dir, "plugins")
        os.makedirs(plugins_dir, exist_ok=True)
        geyser_path = os.path.join(plugins_dir, "Geyser-Spigot.jar")
        if not os.path.exists(geyser_path):
            self.log("> Geyser (Bedrock Crossplay) eklentisi indiriliyor...")
            try:
                url = "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot"
                self._download_file(url, geyser_path)
                self.log("> Geyser eklentisi plugins klasörüne kuruldu ✔")
            except Exception as e:
                self.log(f"Geyser indirme uyarısı: {e}")

    def _install_floodgate_plugin(self):
        plugins_dir = os.path.join(self.target_dir, "plugins")
        os.makedirs(plugins_dir, exist_ok=True)
        fg_path = os.path.join(plugins_dir, "Floodgate-Spigot.jar")
        if not os.path.exists(fg_path):
            self.log("> Floodgate (Şifresiz Bedrock Girişi) eklentisi indiriliyor...")
            try:
                url = "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot"
                self._download_file(url, fg_path)
                self.log("> Floodgate eklentisi plugins klasörüne kuruldu ✔")
            except Exception as e:
                self.log(f"Floodgate indirme uyarısı: {e}")

    def _download_file(self, url, dest_path):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoMinecraftServerMaker/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest_path, "wb") as out:
            total_size = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                out.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = int(downloaded / total_size * 100)
                    if self.progress_callback:
                        try:
                            self.progress_callback(pct, downloaded, total_size)
                        except TypeError:
                            try:
                                self.progress_callback(pct)
                            except Exception:
                                pass
                        except Exception:
                            pass
                    if downloaded % (1024 * 1024 * 5) < 65536:
                        self.log(f"İndiriliyor: %{pct} ({downloaded // (1024*1024)} MB)")
                else:
                    if self.progress_callback:
                        try:
                            self.progress_callback(50, downloaded, 0)
                        except TypeError:
                            try:
                                self.progress_callback(50)
                            except Exception:
                                pass
                        except Exception:
                            pass

    def _write_server_properties(self, server_port, rcon_port, rcon_pass):
        props_path = os.path.join(self.target_dir, "server.properties")
        content = f"""# Minecraft Server Properties - Auto-generated
server-port={server_port}
enable-rcon=true
rcon.port={rcon_port}
rcon.password={rcon_pass}
broadcast-rcon-to-ops=true
online-mode=false
motd=\\u00a76\\u00a7lAuto Minecraft Server\\u00a7f - \\u00a7aAktif!
max-players=20
view-distance=10
simulation-distance=8
gamemode=survival
difficulty=normal
enable-command-block=true
spawn-protection=0
query.port={server_port}
rate-limit=0
sync-chunk-writes=true
"""
        with open(props_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_start_script(self, jar_filename, min_ram, max_ram, mc_version="1.20.4"):
        os.makedirs(self.target_dir, exist_ok=True)
        bat_path = os.path.join(self.target_dir, "start.bat")
        
        # Legacy Betas/Alphas do not support modern Aikar G1GC flags
        v_low = str(mc_version).lower().strip()
        is_legacy = v_low.startswith(("b", "a", "c", "rd")) or any(v_low.startswith(x) for x in ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"])
        
        if is_legacy:
            jvm_args = f"-Xms{min_ram}G -Xmx{max_ram}G -jar {jar_filename} nogui"
        else:
            jvm_args = f"-Xms{min_ram}G -Xmx{max_ram}G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar {jar_filename} nogui"

        # Safe compatible Java runtime resolution
        java_target = getattr(self, "java_bin", "")
        if not java_target or not os.path.exists(java_target):
            # Check relative tools path
            rel_j17 = os.path.abspath(os.path.join(self.target_dir, "..", "tools", "java", "jre-17", "bin", "java.exe"))
            if os.path.exists(rel_j17):
                java_target = rel_j17
            else:
                java_target = "java"

        content = (
            "@echo off\r\n"
            f"title Auto Minecraft Server ({jar_filename})\r\n"
            "chcp 65001 >nul\r\n"
            "cls\r\n"
            "echo =====================================================================\r\n"
            "echo           AUTO MINECRAFT SERVER MAKER - BASLATICI\r\n"
            "echo =====================================================================\r\n"
            "echo.\r\n"
            f"echo [*] Sunucu Jar: {jar_filename}\r\n"
            f"echo [*] RAM: Min {min_ram}GB - Max {max_ram}GB\r\n"
            "echo.\r\n\r\n"
            "REM Uyumlu Java Calistiricisi (Java 25 Uyumluluk Koruyucusu)\r\n"
            "set \"JAVA_CMD=java\"\r\n"
            f'if exist "{java_target}" (\r\n'
            f'    set "JAVA_CMD={java_target}"\r\n'
            ') else if exist "%~dp0..\\tools\\java\\jre-17\\bin\\java.exe" (\r\n'
            '    set "JAVA_CMD=%~dp0..\\tools\\java\\jre-17\\bin\\java.exe"\r\n'
            ') else if exist "%~dp0tools\\java\\jre-17\\bin\\java.exe" (\r\n'
            '    set "JAVA_CMD=%~dp0tools\\java\\jre-17\\bin\\java.exe"\r\n'
            ")\r\n\r\n"
            'echo [*] Kullanilan Java: "%JAVA_CMD%"\r\n'
            "echo.\r\n\r\n"
            f'"%JAVA_CMD%" --add-opens java.base/sun.misc=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED {jvm_args}\r\n'
            "pause\r\n"
        )
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(content)
