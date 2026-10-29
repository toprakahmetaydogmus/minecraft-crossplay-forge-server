# -*- coding: utf-8 -*-
"""
Autonomous Dependency Bootstrapper
Ensures all required runtime packages are installed automatically before launching GUI.
Works seamlessly on any Windows / Linux / macOS PC.
"""

import sys
import subprocess
import importlib

REQUIRED_PACKAGES = {
    "customtkinter": "customtkinter>=6.0.0",
    "requests": "requests>=2.31.0",
    "psutil": "psutil>=5.9.0"
}

def ensure_dependencies():
    """Checks and automatically installs missing dependencies via pip."""
    # Never attempt pip installs inside a packaged PyInstaller frozen executable
    if getattr(sys, "frozen", False):
        return True

    missing = []
    for mod_name, pkg_spec in REQUIRED_PACKAGES.items():

        try:
            importlib.import_module(mod_name)
        except ImportError:
            missing.append(pkg_spec)

    if not missing:
        return True

    print(f"[*] Gerekli paketler eksik tespit edildi, otomatik kuruluyor: {', '.join(missing)}")
    try:
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + missing
        res = subprocess.call(cmd)
        if res == 0:
            print("[+] Tüm bağımlılıklar başarıyla otomatik kuruldu!")
            return True
        else:
            print(f"[-] Pip yükleme uyarısı (kod: {res}), devam ediliyor...")
            return False
    except Exception as e:
        print(f"[-] Otomatik bağımlılık yükleme hatası: {e}")
        return False

if __name__ == "__main__":
    ensure_dependencies()
