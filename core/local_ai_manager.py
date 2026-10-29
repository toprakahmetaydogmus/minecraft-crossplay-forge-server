# -*- coding: utf-8 -*-
"""
Local AI Manager (Ollama Autonomous Integration)
Provides 100% offline, private, zero-API-key AI execution:
- Auto-detects if Ollama is installed on Windows/Linux/macOS
- 1-Click autonomous downloader & installer for Ollama (OllamaSetup.exe)
- Auto-starts Ollama daemon service in the background
- 1-Click autonomous model downloader (llama3.2, qwen2.5, mistral, phi3) with real-time progress streaming
- Zero API keys required, works on any standard computer!
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import urllib.error
import subprocess
import threading
import logging

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_DOWNLOAD_URL = "https://ollama.com/download/OllamaSetup.exe"

POPULAR_LOCAL_MODELS = [
    ("qwen2.5:1.5b", "🚀 Ultra Hızlı & Hafif (1 GB - Her Bilgisayarda Uçar)"),
    ("llama3.2:3b", "⚡ Meta Llama 3.2 (2 GB - Akıllı & Çok Hızlı)"),
    ("llama3.2:1b", "🪶 Süper Minik (1.3 GB - Düşük RAM Uyumlu)"),
    ("llama3:latest", "🧠 Meta Llama 3 (4.7 GB - Yüksek Zekâ)"),
    ("qwen2.5-coder:latest", "💻 Kod & Minecraft Komut Uzmanı (4.7 GB)"),
    ("mistral:latest", "🌪️ Mistral 7B (4.1 GB - Güçlü Mantık)"),
    ("phi3:mini", "🔬 Microsoft Phi-3 Mini (2.2 GB - Kompakt & Keskin)")
]


class LocalAIManager:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback or print

    def log(self, message):
        try:
            self.log_callback(f"[Local AI] {message}")
        except Exception:
            pass

    def get_ollama_path(self):
        """Finds the ollama executable path."""
        p = shutil.which("ollama")
        if p:
            return p

        # Check standard Windows paths
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(local_app_data, "Programs", "Ollama", "ollama.exe"),
            r"C:\Program Files\Ollama\ollama.exe",
            r"C:\Program Files (x86)\Ollama\ollama.exe"
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    def is_installed(self):
        return self.get_ollama_path() is not None

    def is_service_running(self):
        """Checks if http://127.0.0.1:11434 responds."""
        try:
            req = urllib.request.Request(OLLAMA_BASE_URL, headers={"User-Agent": "AutoMinecraftServerMaker"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def ensure_service_running(self):
        """Starts Ollama in background if not already running."""
        if self.is_service_running():
            return True

        ollama_bin = self.get_ollama_path()
        if not ollama_bin:
            self.log("Ollama kurulu değil, otomatik başlatılamadı.")
            return False

        self.log("Ollama arka plan servisi başlatılıyor (ollama serve)...")
        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    [ollama_bin, "serve"],
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen([ollama_bin, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Wait up to 5 seconds for service port to open
            for _ in range(10):
                time.sleep(0.5)
                if self.is_service_running():
                    self.log("✅ Ollama yerel servisi başarıyla aktif edildi!")
                    return True
        except Exception as e:
            self.log(f"Ollama başlatma hatası: {e}")

        return self.is_service_running()

    def download_and_install_ollama(self, status_callback=None):
        """Downloads OllamaSetup.exe and runs installer."""
        temp_dir = os.path.join(os.environ.get("TEMP", os.getcwd()), "OllamaInstall")
        os.makedirs(temp_dir, exist_ok=True)
        setup_exe = os.path.join(temp_dir, "OllamaSetup.exe")

        def _update(msg):
            if status_callback:
                status_callback(msg)
            self.log(msg)

        _update("📥 Ollama resmi kurulum dosyası indiriliyor (ollama.com)...")
        try:
            req = urllib.request.Request(OLLAMA_DOWNLOAD_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp, open(setup_exe, "wb") as out:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    out.write(chunk)
                    downloaded += len(chunk)
                    if total > 0 and downloaded % (1024 * 1024 * 5) < 65536:
                        pct = int(downloaded / total * 100)
                        _update(f"İndiriliyor: %{pct} ({downloaded // (1024*1024)} MB / {total // (1024*1024)} MB)")

            _update("⚙️ Kurulum başlatılıyor, lütfen açılan pencereyi onaylayınız...")
            subprocess.Popen([setup_exe])
            _update("✅ Ollama kurulumu başlatıldı! Kurulum bitince uygulamayı kullanabilirsiniz.")
            return True
        except Exception as e:
            _update(f"❌ İndirme/Kurulum hatası: {e}")
            return False

    def list_local_models(self):
        """Queries http://127.0.0.1:11434/api/tags and returns model list."""
        if not self.ensure_service_running():
            return []

        url = f"{OLLAMA_BASE_URL}/api/tags"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AutoMinecraftServerMaker"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
            return models
        except Exception:
            return []

    def get_status(self):
        """Returns comprehensive status dictionary for UI display."""
        installed = self.is_installed()
        running = self.is_service_running()
        models = self.list_local_models() if running else []
        return {
            "installed": installed,
            "running": running,
            "path": self.get_ollama_path(),
            "models": models
        }

    def pull_model_stream(self, model_name, progress_callback=None):
        """
        Pulls a model from Ollama library with streaming progress.
        progress_callback can receive (percent: int, message: str) or (message: str)
        """
        if not self.ensure_service_running():
            if progress_callback:
                progress_callback(0, "❌ Ollama servisi çalışmıyor veya başlatılamadı.")
            return False

        url = f"{OLLAMA_BASE_URL}/api/pull"
        payload = json.dumps({"name": model_name, "stream": True}).encode("utf-8")
        self.log(f"'{model_name}' yerel modeli indiriliyor...")

        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=3600) as resp:
                for line in resp:
                    if not line:
                        continue
                    try:
                        chunk_data = json.loads(line.decode("utf-8", errors="replace"))
                        status = chunk_data.get("status", "")
                        completed = chunk_data.get("completed", 0)
                        total = chunk_data.get("total", 0)

                        pct = 0
                        if total > 0:
                            pct = int((completed / total) * 100)
                            msg = f"{status}: %{pct} ({completed // (1024*1024)}MB / {total // (1024*1024)}MB)"
                        else:
                            msg = status

                        if progress_callback:
                            try:
                                progress_callback(pct, msg)
                            except TypeError:
                                progress_callback(msg)
                    except Exception:
                        pass

            self.log(f"✅ '{model_name}' modeli başarıyla indirildi ve kullanıma hazır!")
            if progress_callback:
                try:
                    progress_callback(100, f"✅ '{model_name}' modeli hazır!")
                except TypeError:
                    progress_callback(f"✅ '{model_name}' modeli hazır!")
            return True
        except Exception as e:
            err_msg = f"Model indirme hatası: {e}"
            self.log(err_msg)
            if progress_callback:
                try:
                    progress_callback(0, f"❌ {err_msg}")
                except TypeError:
                    progress_callback(f"❌ {err_msg}")
            return False

