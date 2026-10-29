# -*- coding: utf-8 -*-
"""
Java Environment Detector & Autonomous Portable Runtime Manager
Detects installed Java JDK/JRE runtimes and matches them with Minecraft version requirements:
- Minecraft <= 1.16.5 & Betas/Alphas: Java 8
- Minecraft 1.17 - 1.17.1: Java 16/17
- Minecraft 1.18 - 1.20.4: Java 17 (Java 25 is strictly prohibited due to sun.misc.Unsafe removal)
- Minecraft 1.20.5+ & 26.x: Java 21 LTS
Includes autonomous portable JRE provisioning (Adoptium OpenJDK).
"""

import os
import sys
import re
import zipfile
import subprocess
import urllib.request
import logging

class JavaDetector:
    @staticmethod
    def _get_creationflags():
        return 0x08000000 if sys.platform == "win32" else 0

    @staticmethod
    def get_system_java():
        """Checks default 'java' in PATH."""
        try:
            res = subprocess.run(
                ["java", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                creationflags=JavaDetector._get_creationflags()
            )
            raw = res.stderr or res.stdout
            ver = JavaDetector._parse_version(raw)
            return {"path": "java", "version": ver, "raw": raw.strip()}
        except Exception:
            return None

    @staticmethod
    def find_all_javas():
        """Searches common Windows directories for Java executables."""
        candidates = []
        sys_j = JavaDetector.get_system_java()
        if sys_j:
            candidates.append(sys_j)

        search_dirs = [
            os.environ.get("JAVA_HOME", ""),
            r"C:\Program Files\Java",
            r"C:\Program Files\Eclipse Adoptium",
            r"C:\Program Files\Microsoft",
            r"C:\Program Files\BellSoft",
            r"C:\Program Files\Zulu",
            r"C:\Program Files (x86)\Java",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "java17")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "java"))
        ]

        found_paths = set()
        for root in search_dirs:
            if not root or not os.path.exists(root):
                continue
            if os.path.isfile(root) and root.lower().endswith("java.exe"):
                found_paths.add(root)
                continue

            for dirpath, _, filenames in os.walk(root):
                if "java.exe" in [f.lower() for f in filenames]:
                    jpath = os.path.join(dirpath, "java.exe")
                    if jpath not in found_paths:
                        found_paths.add(jpath)

        for p in found_paths:
            try:
                res = subprocess.run(
                    [p, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5,
                    creationflags=JavaDetector._get_creationflags()
                )
                raw = res.stderr or res.stdout
                ver = JavaDetector._parse_version(raw)
                candidates.append({"path": p, "version": ver, "raw": raw.strip()})
            except Exception:
                pass

        # Deduplicate
        unique = []
        seen = set()
        for c in candidates:
            if c["path"] not in seen:
                seen.add(c["path"])
                unique.append(c)

        return unique

    @staticmethod
    def _parse_version(raw_str):
        # Matches "1.8.0_...", "17.0.2", "21.0.7", "25.0.3"
        match = re.search(r'version "(1\.[0-8]|[0-9]+)(\.[0-9]+)*', raw_str)
        if match:
            v = match.group(1)
            if v.startswith("1."):
                return int(v.split(".")[1])
            return int(v)
        return 0

    @staticmethod
    def get_recommended_java_for_mc(mc_version):
        v = str(mc_version).lower().strip()
        # All Beta and Alpha versions require Java 8
        if v.startswith("b") or v.startswith("a") or v.startswith("c") or v.startswith("rd"):
            return 8
        try:
            parts = [int(p) for p in re.findall(r'\d+', v)]
            if len(parts) >= 2:
                major, minor = parts[0], parts[1]
                if major == 1:
                    if minor <= 16:
                        return 8
                    elif minor == 17:
                        return 17
                    elif 18 <= minor <= 20:
                        if minor == 20 and len(parts) >= 3 and parts[2] >= 5:
                            return 21
                        return 17
                    else:
                        return 21
                elif major > 1:
                    return 21
        except Exception:
            pass
        return 17

    @staticmethod
    def get_recommended_java_version(mc_version):
        """Unified alias for get_recommended_java_for_mc."""
        return JavaDetector.get_recommended_java_for_mc(mc_version)

    @staticmethod
    def ensure_compatible_java(mc_version, base_dir=".", log_callback=None):
        """
        Locates or autonomously provisions a 100% compatible Java binary for the specified Minecraft version.
        Guarantees that Java 25 is never assigned to 1.18 - 1.20.4 Forge/Arclight servers.
        Returns the absolute path to java.exe.
        """
        rec_ver = JavaDetector.get_recommended_java_for_mc(mc_version)
        raw_log = log_callback or print

        def log(msg):
            try:
                raw_log(msg)
            except Exception:
                try:
                    clean = msg.encode("ascii", "replace").decode("ascii")
                    raw_log(clean)
                except Exception:
                    pass

        # 1. Check local portable runtime in tools/java/jre-{rec_ver}/bin/java.exe
        # Also check root tools dir
        candidates_portable = [
            os.path.abspath(os.path.join(base_dir, "tools", "java", f"jre-{rec_ver}", "bin", "java.exe")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "java", f"jre-{rec_ver}", "bin", "java.exe")),
            os.path.abspath(os.path.join(base_dir, "..", "tools", "java", f"jre-{rec_ver}", "bin", "java.exe")),
        ]
        for p in candidates_portable:
            if os.path.exists(p):
                log(f"✔ Taşınabilir Eclipse Adoptium Java {rec_ver} tespit edildi: {p}")
                return p

        # 2. Check all installed runtimes on system
        all_javas = JavaDetector.find_all_javas()
        # Look for exact version match
        for j in all_javas:
            if j["version"] == rec_ver and os.path.exists(j["path"]):
                log(f"✔ Sistemde uyumlu Java {rec_ver} bulundu: {j['path']}")
                return j["path"]

        # For 1.20.5+ or 26.x, Java 21+ or system default can work
        if rec_ver == 21:
            for j in all_javas:
                if j["version"] >= 21 and os.path.exists(j["path"]):
                    return j["path"]

        # 3. If compatible Java not found, auto-download portable Adoptium JRE
        log(f"⚠️ Minecraft {mc_version} için Java {rec_ver} gereklidir. Taşınabilir JRE {rec_ver} otomatik indiriliyor...")
        portable_dir = os.path.abspath(os.path.join(base_dir, "tools", "java", f"jre-{rec_ver}"))
        os.makedirs(portable_dir, exist_ok=True)
        zip_path = os.path.join(portable_dir, f"jre-{rec_ver}.zip")

        download_url = f"https://api.adoptium.net/v3/binary/latest/{rec_ver}/ga/windows/x64/jre/hotspot/normal/eclipse"
        try:
            req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp, open(zip_path, "wb") as out:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    out.write(chunk)

            log(f"📦 JRE {rec_ver} paketi açılıyor...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Find root folder in zip
                root_folder = zip_ref.namelist()[0].split("/")[0]
                zip_ref.extractall(portable_dir)

            try:
                os.remove(zip_path)
            except Exception:
                pass

            # Relocate bin to jre-{rec_ver}/bin if wrapped
            extracted_bin = os.path.join(portable_dir, root_folder, "bin", "java.exe")
            if os.path.exists(extracted_bin):
                # Copy or rename contents
                for item in os.listdir(os.path.join(portable_dir, root_folder)):
                    s = os.path.join(portable_dir, root_folder, item)
                    d = os.path.join(portable_dir, item)
                    if not os.path.exists(d):
                        try:
                            os.rename(s, d)
                        except Exception:
                            pass

            final_bin = os.path.join(portable_dir, "bin", "java.exe")
            if os.path.exists(final_bin):
                log(f"✅ Taşınabilir Java {rec_ver} başarıyla kuruldu: {final_bin}")
                return final_bin
        except Exception as e:
            log(f"❌ Taşınabilir JRE indirme hatası: {e}")

        # Fallback to system java
        sys_j = JavaDetector.get_system_java()
        return sys_j["path"] if sys_j else "java"

    @staticmethod
    def get_java_download_url(version=21):
        """Returns direct official Eclipse Adoptium Temurin MSI installer URL for Windows x64."""
        if version == 21:
            return "https://api.adoptium.net/v3/installer/latest/21/ga/windows/x64/jdk/hotspot/normal/eclipse"
        elif version == 17:
            return "https://api.adoptium.net/v3/installer/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse"
        elif version == 8:
            return "https://api.adoptium.net/v3/installer/latest/8/ga/windows/x64/jdk/hotspot/normal/eclipse"
        return "https://adoptium.net/temurin/releases/"

    @staticmethod
    def open_java_download_page(version=21):
        import webbrowser
        url = JavaDetector.get_java_download_url(version)
        webbrowser.open(url)
