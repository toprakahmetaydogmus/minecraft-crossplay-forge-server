# -*- coding: utf-8 -*-
"""
⚔️ AUTO MINECRAFT SERVER MAKER & AI ENGINEER PRO (v3.7.0 ULTRA)
===================================================================================
- Autonomous Minecraft Server Creator (10+ Flavors: Paper, Purpur, Fabric, Forge, NeoForge, Arclight, Mohist, Velocity, Vanilla, BDS)
- 12+ AI Engines Integrated (NVIDIA NIM, OpenRouter, OpenAI, Claude, Gemini, Groq, Mistral, Together, Perplexity, Cohere, DeepSeek, Ollama)
- Autonomous Local Offline AI Hub (1-Click Ollama Setup & Streaming Model Puller)
- 1-Click Global Tunnel (Playit.gg & UPnP - Play with friends without port forwarding)
- 1-Click Plugin & Mod Hub (20+ High-Performance Plugins)
- Visual server.properties Editor
- World Backup & 1-Click Restore Manager
- Master Admin Control Panel (380+ Commands, Universal Block Hub, Themed Shulker Kits)
- Live CPU, RAM & Server Process Telemetry
- 100% Zero-Leak Security Architecture (Isolated Local Vault)
"""

import os
import sys
import time
import socket
import threading
import traceback

# 1. Critical protection for PyInstaller --noconsole where stdout/stderr are None
class NullWriter:
    encoding = "utf-8"
    errors = "replace"
    def write(self, s):
        pass
    def flush(self):
        pass
    def isatty(self):
        return False

if sys.stdout is None:
    sys.stdout = NullWriter()
if sys.stderr is None:
    sys.stderr = NullWriter()

# 2. Global Uncaught Exception Hook for Reliable Debugging
def fatal_excepthook(exc_type, exc_value, exc_traceback):
    err = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    try:
        base = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "app_crash.log"), "w", encoding="utf-8") as f:
            f.write(err)
    except Exception:
        pass
    try:
        from tkinter import messagebox
        messagebox.showerror("Kritik Hata", f"Uygulama çalıştırılırken beklenmeyen bir hata oluştu:\n\n{exc_value}\n\nDetaylar app_crash.log dosyasına kaydedildi.")
    except Exception:
        pass

sys.excepthook = fatal_excepthook

# 3. Single-Instance Mutex Protection (Non-blocking fallback to avoid ephemeral port collisions)
_single_instance_socket = None
def acquire_single_instance_lock():
    global _single_instance_socket
    for p in [49152, 49153, 49154]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", p))
            s.listen(1)
            _single_instance_socket = s
            return True
        except OSError:
            continue
    return True

# 4. Autonomous Dependency Bootstrap (Self-installs missing packages in dev mode only)
try:
    from core.dependency_bootstrap import ensure_dependencies
    ensure_dependencies()
except Exception:
    pass

import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from ui.theme import apply_global_theme
from core.config_manager import ConfigManager
from core.lan_broadcaster import LanBroadcaster
from core.hardware_monitor import HardwareMonitor
from core.i18n import t, I18n

from ui.ctk_tab_installer import CTkTabInstaller
from ui.ctk_tab_ai_engineer import CTkTabAIEngineer
from ui.ctk_tab_tunnel import CTkTabTunnel
from ui.ctk_tab_plugins import CTkTabPlugins
from ui.ctk_tab_properties import CTkTabProperties
from ui.ctk_tab_backup import CTkTabBackup
from ui.ctk_tab_admin_panel import CTkTabAdminPanel
from ui.ctk_tab_settings import CTkTabSettings

# Configure CustomTkinter Global Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AutoMinecraftServerMakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚔️ Auto Minecraft Server Maker & AI Engineer Pro (v4.0.0 Master)")
        self.geometry("1360x920")
        self.minsize(1180, 780)
        self.configure(fg_color=COLOR_BG_DARK)

        # Set window icon
        try:
            base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
            icon_p = os.path.join(base_dir, "app_icon.ico")
            if os.path.exists(icon_p):
                self.iconbitmap(icon_p)
        except Exception:
            pass

        apply_global_theme(self)

        self.config_manager = ConfigManager()
        self.lan_broadcaster = None
        self.active_tab_btn = None
        self.tabs = {}

        # Restore language preference
        saved_lang = self.config_manager.get_server_config().get("language", "tr")
        I18n.set_language(saved_lang)

        self._build_layout()
        self._start_background_workers()

    def _build_layout(self):
        # Ana Izgara: Sol Sidebar (270px) + Sağ İçerik Alanı
        self.grid_columnconfigure(0, weight=0, minsize=270)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. SOL SIDEBAR
        self.sidebar = ctk.CTkFrame(self, fg_color=COLOR_BG_SIDEBAR, corner_radius=0, width=270)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_propagate(False)

        # Sidebar Logo / Başlık Kartı
        logo_f = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_f.pack(fill="x", padx=16, pady=(16, 8))

        # Üst Dil Seçim Butonu
        top_row = ctk.CTkFrame(logo_f, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(
            top_row,
            text="⚡ AUTO MC",
            font=FONT_TITLE,
            text_color=COLOR_ACCENT_CYAN,
            anchor="w"
        ).pack(side="left")

        self.btn_lang = ctk.CTkButton(
            top_row,
            text=f"🌐 {I18n.get_language().upper()} (TR/EN)",
            font=("Segoe UI", 9, "bold"),
            width=84,
            height=22,
            fg_color="#1e293b",
            hover_color="#334155",
            text_color=COLOR_ACCENT_GOLD,
            corner_radius=11,
            command=self._toggle_language
        )
        self.btn_lang.pack(side="right")

        ctk.CTkLabel(
            logo_f,
            text="SERVER MAKER PRO",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_MAIN,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_f,
            text="v3.9.0 ULTIMATE • AI Autonomous & Global Multi-Engine",
            font=FONT_SMALL,
            text_color=COLOR_ACCENT_GREEN,
            anchor="w"
        ).pack(anchor="w")

        # Canlı Sunucu Durumu Rozeti
        self.status_badge = ctk.CTkLabel(
            self.sidebar,
            text="● KONTROL EDILIYOR...",
            font=FONT_BOLD,
            text_color=COLOR_ACCENT_GOLD,
            fg_color="#2a2312",
            corner_radius=6,
            height=32
        )
        self.status_badge.pack(fill="x", padx=14, pady=(0, 12))

        # Navigasyon Butonları & Kategorileri
        self.nav_btns = {}
        self.nav_items_meta = [
            ("installer", "nav_installer", self._show_installer),
            ("admin", "nav_admin_panel", self._show_admin),
            ("properties", "nav_properties", self._show_properties),
            ("tunnel", "nav_tunnel", self._show_tunnel),
            ("plugins", "nav_plugins", self._show_plugins),
            ("backup", "nav_backup", self._show_backup),
            ("ai", "nav_ai_engineer", self._show_ai),
            ("settings", "nav_settings", self._show_settings)
        ]

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=12, pady=(0, 10))

        for key, i18n_key, cmd in self.nav_items_meta:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=t(i18n_key),
                font=FONT_BOLD,
                anchor="w",
                height=36,
                corner_radius=8,
                fg_color="transparent",
                text_color=COLOR_TEXT_MAIN,
                hover_color=COLOR_BG_CARD_HOVER,
                command=cmd
            )
            btn.pack(fill="x", pady=2)
            self.nav_btns[key] = (btn, i18n_key)

        # Alt Donanım Telemetrisi Kartı
        tele_card = ctk.CTkFrame(self.sidebar, fg_color=COLOR_BG_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        tele_card.pack(side="bottom", fill="x", padx=12, pady=14)

        ctk.CTkLabel(tele_card, text="📊 CANLI DONANIM TELEMETRİSİ", font=FONT_SMALL, text_color=COLOR_ACCENT_CYAN).pack(anchor="w", padx=10, pady=(8, 4))

        self.lbl_cpu = ctk.CTkLabel(tele_card, text="CPU: %0", font=FONT_SMALL, text_color=COLOR_TEXT_MAIN)
        self.lbl_cpu.pack(anchor="w", padx=10, pady=1)

        self.lbl_ram = ctk.CTkLabel(tele_card, text="RAM: 0GB / 0GB", font=FONT_SMALL, text_color=COLOR_TEXT_MAIN)
        self.lbl_ram.pack(anchor="w", padx=10, pady=1)

        self.ram_progress = ctk.CTkProgressBar(tele_card, height=6, progress_color=COLOR_ACCENT_GREEN)
        self.ram_progress.set(0.3)
        self.ram_progress.pack(fill="x", padx=10, pady=(4, 8))

        # 2. SAĞ İÇERİK ALANI
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=16, pady=14)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Varsayılan sekme: Sunucu Kurucu
        self._show_installer()

    def _toggle_language(self):
        cur = I18n.get_language()
        new_lang = "en" if cur == "tr" else "tr"
        I18n.set_language(new_lang)
        cfg = self.config_manager.get_server_config()
        cfg["language"] = new_lang
        self.config_manager.save_config()
        self.btn_lang.configure(text=f"🌐 {new_lang.upper()} (TR/EN)")
        self._refresh_nav_labels()

    def _refresh_nav_labels(self):
        for key, (btn, i18n_key) in self.nav_btns.items():
            btn.configure(text=t(i18n_key))

    def _switch_tab(self, key):
        # Lazy Loading: Sadece tıklandığında sekme örneğini oluştur
        if key not in self.tabs:
            tab_factories = {
                "installer": lambda: CTkTabInstaller(self.content_area, self.config_manager),
                "ai": lambda: CTkTabAIEngineer(self.content_area, self.config_manager),
                "tunnel": lambda: CTkTabTunnel(self.content_area, self.config_manager),
                "plugins": lambda: CTkTabPlugins(self.content_area, self.config_manager),
                "properties": lambda: CTkTabProperties(self.content_area, self.config_manager),
                "backup": lambda: CTkTabBackup(self.content_area, self.config_manager),
                "admin": lambda: CTkTabAdminPanel(self.content_area, self.config_manager),
                "settings": lambda: CTkTabSettings(self.content_area, self.config_manager)
            }
            if key in tab_factories:
                self.tabs[key] = tab_factories[key]()

        for k, view in self.tabs.items():
            btn = self.nav_btns[k][0] if k in self.nav_btns else None
            if k == key:
                view.grid(row=0, column=0, sticky="nsew")
                if btn:
                    btn.configure(fg_color=COLOR_ACCENT_CYAN, text_color="#000000")
            else:
                view.grid_forget()
                if btn:
                    btn.configure(fg_color="transparent", text_color=COLOR_TEXT_MAIN)

    def _show_installer(self): self._switch_tab("installer")
    def _show_ai(self): self._switch_tab("ai")
    def _show_tunnel(self): self._switch_tab("tunnel")
    def _show_plugins(self): self._switch_tab("plugins")
    def _show_properties(self): self._switch_tab("properties")
    def _show_backup(self): self._switch_tab("backup")
    def _show_admin(self): self._switch_tab("admin")
    def _show_settings(self): self._switch_tab("settings")

    def _start_background_workers(self):
        # 1. LAN Broadcaster (Yerel ağ ve VPN - Radmin/Hamachi otomatik yayın)
        srv_cfg = self.config_manager.get_server_config()
        self.lan_broadcaster = LanBroadcaster(port=srv_cfg.get("server_port", 25565))
        self.lan_broadcaster.start()

        # 2. Donanım & Sunucu Durum İzleyici Worker
        threading.Thread(target=self._telemetry_worker, daemon=True).start()

    def _telemetry_worker(self):
        while True:
            srv_cfg = self.config_manager.get_server_config()
            port = srv_cfg.get("server_port", 25565)

            # Check server port
            is_online = False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                res = s.connect_ex(("127.0.0.1", port))
                s.close()
                is_online = (res == 0)
            except Exception:
                is_online = False

            # Check hardware metrics
            m = HardwareMonitor.get_system_metrics()

            def _update_ui():
                if not self.winfo_exists():
                    return
                if is_online:
                    self.status_badge.configure(text=f"● SUNUCU AKTİF (Port: {port})", text_color=COLOR_ACCENT_GREEN, fg_color="#064e3b")
                else:
                    self.status_badge.configure(text="● SUNUCU KAPALI", text_color=COLOR_ACCENT_RED, fg_color="#450a0a")

                self.lbl_cpu.configure(text=f"CPU: %{m['cpu_percent']}")
                self.lbl_ram.configure(text=f"RAM: {m['ram_used_gb']}GB / {m['ram_total_gb']}GB")
                self.ram_progress.set(m['ram_percent'] / 100.0)

            try:
                self.after(0, _update_ui)
            except Exception:
                break
            time.sleep(2.5)


def main():
    # Enforce Single-Instance Mutex
    if not acquire_single_instance_lock():
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Zaten Çalışıyor",
                "Auto Minecraft Server Maker zaten arka planda veya görev çubuğunda çalışıyor!\nLütfen açık olan pencereyi kullanın."
            )
            root.destroy()
        except Exception:
            pass
        sys.exit(0)

    try:
        app = AutoMinecraftServerMakerApp()
        app.mainloop()
    except Exception as e:
        import traceback
        err_msg = f"Uygulama çalışırken beklenmedik bir hata oluştu:\n\n{e}\n\nDetay:\n{traceback.format_exc()}"
        with open("crash_reason.log", "w", encoding="utf-8") as f:
            f.write(err_msg)
        try:
            messagebox.showerror("Kritik Hata", err_msg)
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()

