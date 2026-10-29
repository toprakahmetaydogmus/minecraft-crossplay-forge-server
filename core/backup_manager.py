# -*- coding: utf-8 -*-
"""
Autonomous Server & World Backup Manager
Creates timestamped compressed .zip archives of worlds and configurations.
Supports 1-click restore.
"""

import os
import shutil
import zipfile
import time
from datetime import datetime

class BackupManager:
    def __init__(self, server_dir, log_callback=None):
        self.server_dir = os.path.abspath(server_dir)
        self.backup_dir = os.path.join(self.server_dir, "backups")
        self.log_callback = log_callback or print

    def log(self, msg):
        try:
            self.log_callback(f"[Yedekleme] {msg}")
        except Exception:
            pass

    def list_backups(self):
        """Returns list of existing backup zip files with size and date."""
        if not os.path.exists(self.backup_dir):
            return []
        files = [f for f in os.listdir(self.backup_dir) if f.lower().endswith(".zip")]
        backups = []
        for f in files:
            fp = os.path.join(self.backup_dir, f)
            stat = os.stat(fp)
            mb = round(stat.st_size / (1024 * 1024), 2)
            dt = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            backups.append({"filename": f, "path": fp, "size_mb": mb, "date": dt})
        backups.sort(key=lambda x: x["date"], reverse=True)
        return backups

    def create_backup(self, include_plugins=True, progress_callback=None):
        """Creates a timestamped .zip archive of the server."""
        os.makedirs(self.backup_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"backup_{ts}.zip"
        zip_path = os.path.join(self.backup_dir, zip_name)

        targets = ["world", "world_nether", "world_the_end", "server.properties", "ops.json", "whitelist.json"]
        if include_plugins:
            targets.append("plugins")

        self.log(f"Yedekleme başlatılıyor: {zip_name}...")
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for target in targets:
                    src = os.path.join(self.server_dir, target)
                    if not os.path.exists(src):
                        continue
                    if os.path.isdir(src):
                        for root, _, files in os.walk(src):
                            # Skip backups inside target dir
                            if "backups" in root:
                                continue
                            for f in files:
                                full_p = os.path.join(root, f)
                                rel_p = os.path.relpath(full_p, self.server_dir)
                                zipf.write(full_p, rel_p)
                    else:
                        zipf.write(src, os.path.basename(src))

            mb = round(os.path.getsize(zip_path) / (1024 * 1024), 2)
            self.log(f"✅ Yedekleme tamamlandı: {zip_name} ({mb} MB)")
            return True
        except Exception as e:
            self.log(f"❌ Yedekleme hatası: {e}")
            return False

    def restore_backup(self, zip_filename):
        """Restores a backup zip into the server directory."""
        zip_path = os.path.join(self.backup_dir, zip_filename)
        if not os.path.exists(zip_path):
            self.log(f"Yedek dosyası bulunamadı: {zip_filename}")
            return False

        self.log(f"Geri yükleme yapılıyor: {zip_filename}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(self.server_dir)
            self.log("✅ Sunucu dünyası ve ayarları başarıyla geri yüklendi!")
            return True
        except Exception as e:
            self.log(f"❌ Geri yükleme hatası: {e}")
            return False
