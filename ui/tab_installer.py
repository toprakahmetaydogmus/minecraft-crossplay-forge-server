# -*- coding: utf-8 -*-
"""
Tab: Automated Server Installer & Launcher
"""

import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ui.theme import *
from core.server_installer import ServerInstaller
from core.java_detector import JavaDetector

class TabInstaller:
    def __init__(self, parent, config_manager, log_callback=None):
        self.parent = parent
        self.config_manager = config_manager
        self.log_callback = log_callback
        self.frame = tk.Frame(parent, bg=BG_DARK)
        self.server_process = None

        self._build_ui()

    def _build_ui(self):
        # Sol Panel: Ayarlar ve Kurulum Kontrolleri
        left_panel = tk.Frame(self.frame, bg=BG_PANEL, width=420, padx=16, pady=16)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        title = tk.Label(
            left_panel,
            text="🚀 OTOMATİK SUNUCU KURUCU",
            font=("Segoe UI", 12, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_PANEL
        )
        title.pack(anchor="w", pady=(0, 12))

        # Sürüm Seçimi
        lbl_ver = tk.Label(left_panel, text="📌 Minecraft Sürümü:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL)
        lbl_ver.pack(anchor="w", pady=(4, 2))

        self.ver_var = tk.StringVar(value="1.20.1")
        self.ver_combo = ttk.Combobox(
            left_panel,
            textvariable=self.ver_var,
            font=("Segoe UI", 9),
            values=["1.21.4", "1.21.1", "1.20.4", "1.20.1", "1.19.4", "1.18.2", "1.16.5", "1.12.2"]
        )
        self.ver_combo.pack(fill=tk.X, pady=(0, 10))

        # Sunucu Türü
        lbl_type = tk.Label(left_panel, text="⚙️ Sunucu Yazılımı (Flavor):", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL)
        lbl_type.pack(anchor="w", pady=(4, 2))

        self.type_var = tk.StringVar(value="Paper")
        self.type_combo = ttk.Combobox(
            left_panel,
            textvariable=self.type_var,
            font=("Segoe UI", 9),
            values=["Paper", "Purpur", "Fabric", "Arclight (Forge+Plugins)", "Vanilla"],
            state="readonly"
        )
        self.type_combo.pack(fill=tk.X, pady=(0, 10))

        # RAM Ayarları
        lbl_ram = tk.Label(left_panel, text="💾 Bellek (RAM) Ayarı:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL)
        lbl_ram.pack(anchor="w", pady=(4, 2))

        ram_frame = tk.Frame(left_panel, bg=BG_PANEL)
        ram_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(ram_frame, text="Min:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        self.min_ram_var = tk.StringVar(value="4")
        self.min_ram_combo = ttk.Combobox(ram_frame, textvariable=self.min_ram_var, width=4, values=["2", "4", "6", "8", "12", "16"])
        self.min_ram_combo.pack(side=tk.LEFT, padx=(4, 12))

        tk.Label(ram_frame, text="Max:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL).pack(side=tk.LEFT)
        self.max_ram_var = tk.StringVar(value="6")
        self.max_ram_combo = ttk.Combobox(ram_frame, textvariable=self.max_ram_var, width=4, values=["4", "6", "8", "10", "12", "16", "24"])
        self.max_ram_combo.pack(side=tk.LEFT, padx=(4, 0))

        # Geyser Crossplay (Bedrock)
        self.geyser_var = tk.BooleanVar(value=True)
        chk_geyser = tk.Checkbutton(
            left_panel,
            text="📱 Bedrock Crossplay (Geyser)",
            variable=self.geyser_var,
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_GREEN,
            bg=BG_PANEL,
            selectcolor=BG_DARK,
            activebackground=BG_PANEL,
            activeforeground=ACCENT_GREEN
        )
        chk_geyser.pack(anchor="w", pady=(4, 10))

        # Java Algılama Durumu
        lbl_j = tk.Label(left_panel, text="☕ Algılanan Java Sürümü:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL)
        lbl_j.pack(anchor="w", pady=(4, 2))

        sys_j = JavaDetector.get_system_java()
        j_text = f"Java {sys_j['version']} (Sistem)" if sys_j and sys_j['version'] > 0 else "Java Bulunamadı ⚠️"
        j_color = ACCENT_GREEN if sys_j and sys_j['version'] >= 17 else ACCENT_RED

        self.java_lbl = tk.Label(left_panel, text=j_text, font=("Segoe UI", 8, "bold"), fg=j_color, bg=BG_CARD, padx=8, pady=4)
        self.java_lbl.pack(fill=tk.X, pady=(0, 14))

        # Kurulum Butonu
        btn_install = tk.Button(
            left_panel,
            text="⚡ TEK TIKLA İNDİR & KUR",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_CYAN,
            fg="#000000",
            activebackground="#0284c7",
            relief=tk.FLAT,
            pady=8,
            command=self.start_installation
        )
        btn_install.pack(fill=tk.X, pady=(0, 8))

        # Başlat / Kapat Butonları
        ctrl_frame = tk.Frame(left_panel, bg=BG_PANEL)
        ctrl_frame.pack(fill=tk.X, pady=(8, 0))

        btn_start = tk.Button(
            ctrl_frame,
            text="▶️ Başlat",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_GREEN,
            fg="#000000",
            relief=tk.FLAT,
            pady=6,
            command=self.start_server
        )
        btn_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        btn_stop = tk.Button(
            ctrl_frame,
            text="⏹️ Durdur",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_RED,
            fg="#ffffff",
            relief=tk.FLAT,
            pady=6,
            command=self.stop_server
        )
        btn_stop.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # Sağ Panel: Kurulum Logları & Konsol
        right_panel = tk.Frame(self.frame, bg=BG_PANEL, padx=14, pady=14)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        log_head = tk.Frame(right_panel, bg=BG_PANEL)
        log_head.pack(fill=tk.X, pady=(0, 6))

        tk.Label(log_head, text="📜 KURULUM & SUNUCU GÜNLÜĞÜ", font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL).pack(side=tk.LEFT)

        btn_clear = tk.Button(log_head, text="Temizle", font=("Segoe UI", 7), bg=BG_CARD, fg=TEXT_MUTED, relief=tk.FLAT, padx=6, command=lambda: self.console.delete("1.0", tk.END))
        btn_clear.pack(side=tk.RIGHT)

        self.console = scrolledtext.ScrolledText(
            right_panel,
            bg="#030712",
            fg="#e2e8f0",
            insertbackground=ACCENT_CYAN,
            font=("Consolas", 9),
            relief=tk.FLAT
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.tag_config("info", foreground="#38bdf8")
        self.console.tag_config("success", foreground=ACCENT_GREEN)
        self.console.tag_config("error", foreground=ACCENT_RED)
        self.console.tag_config("warn", foreground=ACCENT_GOLD)

    def log(self, text, tag="info"):
        self.console.insert(tk.END, f"{text}\n", tag)
        self.console.see(tk.END)

    def start_installation(self):
        cfg = self.config_manager.get_server_config()
        sdir = cfg.get("server_dir", os.path.join(os.getcwd(), "server"))

        ver = self.ver_var.get().strip()
        stype = self.type_var.get().strip()
        min_r = int(self.min_ram_var.get().strip() or "4")
        max_r = int(self.max_ram_var.get().strip() or "6")
        r_port = cfg.get("rcon_port", 25575)
        r_pass = cfg.get("rcon_password", "admin123")
        s_port = cfg.get("server_port", 25565)
        b_port = cfg.get("bedrock_port", 19132)
        geyser = self.geyser_var.get()

        def _worker():
            installer = ServerInstaller(sdir, log_callback=lambda msg: self.parent.after(0, self.log, msg, "info"))
            success = installer.setup_server(
                server_type=stype,
                mc_version=ver,
                min_ram=min_r,
                max_ram=max_r,
                rcon_port=r_port,
                rcon_pass=r_pass,
                server_port=s_port,
                bedrock_port=b_port,
                install_geyser=geyser
            )
            if success:
                self.parent.after(0, self.log, "🎉 Kurulum başarıyla tamamlandı!", "success")
            else:
                self.parent.after(0, self.log, "❌ Kurulum sırasında bir hata oluştu.", "error")

        threading.Thread(target=_worker, daemon=True).start()

    def start_server(self):
        cfg = self.config_manager.get_server_config()
        sdir = cfg.get("server_dir", os.path.join(os.getcwd(), "server"))
        bat_file = os.path.join(sdir, "start.bat")
        if not os.path.exists(bat_file):
            messagebox.showerror("Hata", f"Başlatıcı dosyası bulunamadı:\n{bat_file}\nÖnce sunucuyu kurunuz.")
            return

        self.log(f"[*] Sunucu başlatılıyor: {bat_file}", "info")
        threading.Thread(target=lambda: subprocess.Popen(["cmd.exe", "/c", "start", "", bat_file], cwd=sdir), daemon=True).start()

    def stop_server(self):
        cfg = self.config_manager.get_server_config()
        sdir = cfg.get("server_dir", os.path.join(os.getcwd(), "server"))
        self.log("[*] Sunucu durdurma komutu (RCON üzerinden veya stop.bat)...", "warn")
        # Can trigger RCON stop command or graceful stop
        from core.rcon_client import MinecraftRcon
        rcon = MinecraftRcon(
            host=cfg.get("rcon_host", "127.0.0.1"),
            port=cfg.get("rcon_port", 25575),
            password=cfg.get("rcon_password", "admin123")
        )
        def _stop():
            res = rcon.send_command("stop")
            self.parent.after(0, self.log, f">> {res}", "success" if "Stopping" in res else "warn")
        threading.Thread(target=_stop, daemon=True).start()
