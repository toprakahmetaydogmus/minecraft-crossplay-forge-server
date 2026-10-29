# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: Autonomous Server Installer & Launcher Pro
Incorporates all features:
- "RAKAMLARA BAK" 4-Metric Showcase Banner
- "🤖 AI OTONOM KURULUM ASİSTANI" (AI Autonomous Server Setup Wizard)
- 10+ Server Flavors with 1-Click Pill Selector
- 1.0.0 -> 1.21.4+ Complete Legacy-to-Modern Version Matrix + Custom Version Input
- Dynamic Java Compatibility Watcher & 1-Click Adoptium Java JRE Downloader
- macOS/Linux Style Developer Terminal with Live Progress Bar
- Glowing "SUNUCU ÇALIŞIYOR" Status Indicator
- "Yapay Zekâ Çökme Doktoru" (AI Crash Doctor)
- Bedrock & Console Crossplay (Geyser + Floodgate)
- Bilingual Support (TR / EN) via core.i18n
"""

import os
import time
import socket
import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.server_installer import ServerInstaller
from core.java_detector import JavaDetector
from core.ai_engineer import AIEngineer
from core.i18n import t, I18n

class CTkTabInstaller(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        self.ai_engineer = AIEngineer(config_manager)
        self.server_process = None
        self.flavor_pills = {}

        self._build_ui()
        self._update_java_status()
        self._start_server_watcher()
        I18n.register_listener(self._on_language_changed)

    def _on_language_changed(self, lang):
        # Refresh dynamic texts
        try:
            self.lbl_title.configure(text=t("installer_title"))
            self.lbl_flavors.configure(text=t("installer_flavor_label"))
            self.lbl_versions.configure(text=t("installer_version_label"))
            self.lbl_java_head.configure(text=t("installer_java_status"))
            self.btn_download_java.configure(text=t("installer_java_btn"))
            self.lbl_ram_head.configure(text=t("installer_ram_label"))
            self.geyser_switch.configure(text=t("installer_crossplay"))
            self.btn_install.configure(text=t("installer_btn_install"))
            self.btn_start.configure(text=t("installer_btn_start"))
            self.btn_stop.configure(text=t("installer_btn_stop"))
            self.ai_wizard_btn.configure(text=t("ai_wizard_btn_run"))
        except Exception:
            pass

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(1, weight=1)

        # =====================================================================
        # ÜST BANNER: "RAKAMLARA BAK" (4-KART METRİK VİTRİNİ)
        # =====================================================================
        stats_banner = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        stats_banner.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 10))

        for col_idx in range(4):
            stats_banner.grid_columnconfigure(col_idx, weight=1)

        metrics = [
            ("10+ SUNUCU TÜRÜ", "Paper • Purpur • Fabric • Forge...", COLOR_ACCENT_GREEN),
            ("1.0 ➔ 1.21.4+", "Tüm Sürümler (Eskiden Yeniye)", COLOR_ACCENT_CYAN),
            ("12 AI MOTORU", "Ollama, Groq, DeepSeek & Yerel", COLOR_ACCENT_PURPLE),
            ("380+ ADMİN KOMUTU", "300+ Blok • 16 Kategori Sekmesi", COLOR_ACCENT_GOLD),
        ]

        for idx, (title, sub, color) in enumerate(metrics):
            card = ctk.CTkFrame(stats_banner, fg_color=COLOR_BG_CARD_HOVER, corner_radius=8, border_width=1, border_color=color)
            card.grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")

            ctk.CTkLabel(card, text=title, font=("Segoe UI", 11, "bold"), text_color=color).pack(anchor="center", pady=(6, 1))
            ctk.CTkLabel(card, text=sub, font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(anchor="center", pady=(0, 6))

        # =====================================================================
        # SOL KART: Kurulum Parametreleri & 1-Tıkla Pill Seçici & AI Asistanı
        # =====================================================================
        left_card = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=0)

        self.lbl_title = ctk.CTkLabel(left_card, text=t("installer_title"), font=FONT_SUBTITLE, text_color=COLOR_ACCENT_CYAN)
        self.lbl_title.pack(anchor="w", pady=(4, 8))

        # ---------------------------------------------------------------------
        # 🤖 AI OTONOM KURULUM ASİSTANI KARTI
        # ---------------------------------------------------------------------
        ai_box = ctk.CTkFrame(left_card, fg_color="#0f172a", corner_radius=10, border_width=1, border_color=COLOR_ACCENT_PURPLE)
        ai_box.pack(fill="x", pady=(0, 12), padx=2)

        ctk.CTkLabel(ai_box, text=t("ai_wizard_title"), font=("Segoe UI", 12, "bold"), text_color=COLOR_ACCENT_PURPLE).pack(anchor="w", padx=10, pady=(8, 2))
        ctk.CTkLabel(ai_box, text=t("ai_wizard_desc"), font=("Segoe UI", 9), text_color=COLOR_TEXT_MUTED, wraplength=340, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        self.ai_prompt_var = ctk.StringVar()
        self.ai_prompt_entry = ctk.CTkEntry(
            ai_box,
            textvariable=self.ai_prompt_var,
            placeholder_text=t("ai_wizard_placeholder"),
            font=FONT_SMALL,
            fg_color=COLOR_BG_CARD_HOVER,
            border_color=COLOR_BORDER,
            height=32
        )
        self.ai_prompt_entry.pack(fill="x", padx=10, pady=(0, 6))
        self.ai_prompt_entry.bind("<Return>", lambda e: self._run_ai_wizard())

        # Hızlı Senaryo Çipleri (Quick Chips)
        chips_frame = ctk.CTkFrame(ai_box, fg_color="transparent")
        chips_frame.pack(fill="x", padx=10, pady=(0, 8))

        chips = [
            ("⚔️ 1.20.1 Büyü & Kılıç", "1.20.1 Forge büyü kılıç modu ve harita kur 6gb ram"),
            ("🗺️ 1.20.4 Fabric Harita & FPS", "1.20.4 hafif Fabric harita ve optimizasyon modları kur 4gb ram"),
            ("🧟 1.20.1 Zombi Kıyameti", "1.20.1 zombi kıyameti ve hayatta kalma modlu sunucu kur 6gb ram"),
            ("⚙️ 1.20.1 Create & Teknoloji", "1.20.1 Forge create teknoloji ve depolama modlu sunucu kur 6gb ram"),
            ("📱 1.21.1 Crossplay", "1.21.1 Bedrock ve Java mobil crossplay Geyser sunucusu kur"),
            ("🔥 26.3 En Son Sürüm", "26.3 Wilderness Bound en son stabil sunucu kur 4GB RAM")
        ]

        for chip_text, chip_prompt in chips:
            btn_chip = ctk.CTkButton(
                chips_frame,
                text=chip_text,
                font=("Segoe UI", 9),
                height=22,
                fg_color=COLOR_BG_CARD_HOVER,
                hover_color=COLOR_ACCENT_PURPLE,
                text_color=COLOR_TEXT_MAIN,
                corner_radius=11,
                command=lambda p=chip_prompt: self._apply_and_run_ai_chip(p)
            )
            btn_chip.pack(side="left", padx=2, pady=2)

        self.ai_wizard_btn = ctk.CTkButton(
            ai_box,
            text=t("ai_wizard_btn_run"),
            font=("Segoe UI", 11, "bold"),
            fg_color=COLOR_ACCENT_PURPLE,
            hover_color="#9333ea",
            text_color="#ffffff",
            height=32,
            corner_radius=6,
            command=self._run_ai_wizard
        )
        self.ai_wizard_btn.pack(fill="x", padx=10, pady=(0, 10))

        # ---------------------------------------------------------------------
        # 1. 10+ Sunucu Türü Pill Seçici
        # ---------------------------------------------------------------------
        self.lbl_flavors = ctk.CTkLabel(left_card, text=t("installer_flavor_label"), font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.lbl_flavors.pack(anchor="w", pady=(2, 4))
        
        pills_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        pills_frame.pack(fill="x", pady=(0, 10))
        for p_col in range(3):
            pills_frame.grid_columnconfigure(p_col, weight=1)

        flavor_list = [
            ("PaperMC", "PaperMC (Yüksek Performans)"),
            ("Purpur", "Purpur (Optimize & Özellik Zengin)"),
            ("Fabric", "Fabric (Hafif & Hızlı Modlu)"),
            ("Arclight", "Arclight (Forge + Plugin Hibrit)"),
            ("Mohist", "Mohist (Forge + Bukkit Alternatif)"),
            ("Forge", "Forge (Klasik Modlu)"),
            ("NeoForge", "NeoForge (Yeni Nesil Modlu 1.20.4+)"),
            ("Velocity", "Velocity (Yeni Nesil Proxy)"),
            ("Vanilla", "Vanilla (Resmi Saf Mojang)")
        ]

        self.flavor_var = ctk.StringVar(value="PaperMC (Yüksek Performans)")

        for p_idx, (short_name, full_name) in enumerate(flavor_list):
            r = p_idx // 3
            c = p_idx % 3
            btn = ctk.CTkButton(
                pills_frame,
                text=short_name,
                font=FONT_SMALL,
                height=28,
                corner_radius=6,
                fg_color=COLOR_ACCENT_CYAN if p_idx == 0 else COLOR_BG_CARD_HOVER,
                text_color="#000000" if p_idx == 0 else COLOR_TEXT_MAIN,
                hover_color=COLOR_ACCENT_CYAN,
                command=lambda fn=full_name, sn=short_name: self._select_flavor(fn, sn)
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="ew")
            self.flavor_pills[short_name] = btn

        # ---------------------------------------------------------------------
        # 2. Minecraft Sürümü (Modern, Klasik, Betalar & Özel Giriş)
        # ---------------------------------------------------------------------
        self.lbl_versions = ctk.CTkLabel(left_card, text=t("installer_version_label"), font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.lbl_versions.pack(anchor="w", pady=(2, 2))

        # Sürüm Kategori Filtre Butonları (2 Satır)
        ver_cat_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        ver_cat_frame.pack(fill="x", pady=(0, 2))

        row_cat1 = ctk.CTkFrame(ver_cat_frame, fg_color="transparent")
        row_cat1.pack(fill="x", pady=(0, 2))
        for cat_key, cat_label, cat_color in [
            ("drops", "🔥 26.x", "#f97316"),
            ("modern_121", "⭐ 1.21", COLOR_ACCENT_CYAN),
            ("modern_120", "💎 1.20", COLOR_ACCENT_GREEN),
            ("golden", "🌿 1.16-1.19", "#38bdf8")
        ]:
            ctk.CTkButton(
                row_cat1,
                text=cat_label,
                font=("Segoe UI", 8, "bold"),
                height=22,
                fg_color=COLOR_BG_CARD_HOVER,
                hover_color=cat_color,
                command=lambda c=cat_key: self._filter_version_category(c)
            ).pack(side="left", padx=1, expand=True, fill="x")

        row_cat2 = ctk.CTkFrame(ver_cat_frame, fg_color="transparent")
        row_cat2.pack(fill="x", pady=(0, 4))
        for cat_key, cat_label, cat_color in [
            ("classic", "🏰 1.0-1.15", COLOR_ACCENT_GOLD),
            ("betas", "🧪 Beta", COLOR_ACCENT_PURPLE),
            ("alphas", "📜 Alfa", "#ec4899"),
            ("infdev_classic", "🏛️ Klasik", "#a855f7"),
            ("all", "⚡ Tümü", COLOR_ACCENT_GREEN)
        ]:
            ctk.CTkButton(
                row_cat2,
                text=cat_label,
                font=("Segoe UI", 8, "bold"),
                height=22,
                fg_color=COLOR_BG_CARD_HOVER,
                hover_color=cat_color,
                command=lambda c=cat_key: self._filter_version_category(c)
            ).pack(side="left", padx=1, expand=True, fill="x")

        all_versions = ServerInstaller.get_supported_versions("modern_121")

        self.ver_var = ctk.StringVar(value=all_versions[0] if all_versions else "1.21.4 (The Garden Awakens)")
        self.ver_menu = ctk.CTkOptionMenu(
            left_card,
            variable=self.ver_var,
            values=all_versions,
            fg_color=COLOR_BG_CARD_HOVER,
            button_color=COLOR_ACCENT_CYAN,
            button_hover_color="#0284c7",
            command=lambda v: self._update_java_status()
        )
        self.ver_menu.pack(fill="x", pady=(0, 4))

        # Özel Sürüm / Snapshot Elle Giriş Satırı
        custom_ver_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        custom_ver_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(custom_ver_frame, text=t("installer_custom_version"), font=("Segoe UI", 9), text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))
        self.custom_ver_var = ctk.StringVar()
        self.custom_ver_entry = ctk.CTkEntry(
            custom_ver_frame,
            textvariable=self.custom_ver_var,
            placeholder_text="örn: 1.5.2, 1.21.3...",
            font=FONT_SMALL,
            height=24,
            width=140,
            fg_color=COLOR_BG_CARD_HOVER
        )
        self.custom_ver_entry.pack(side="left", fill="x", expand=True)
        self.custom_ver_entry.bind("<KeyRelease>", self._on_custom_ver_changed)

        # ---------------------------------------------------------------------
        # 3. Java Durumu ve Uyuşmazlık Çözümü
        # ---------------------------------------------------------------------
        self.lbl_java_head = ctk.CTkLabel(left_card, text=t("installer_java_status"), font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.lbl_java_head.pack(anchor="w", pady=(2, 2))
        
        self.java_badge_frame = ctk.CTkFrame(left_card, fg_color=COLOR_BG_CARD_HOVER, corner_radius=6)
        self.java_badge_frame.pack(fill="x", pady=(0, 10))

        self.lbl_java_info = ctk.CTkLabel(self.java_badge_frame, text="Kontrol ediliyor...", font=FONT_SMALL, text_color=COLOR_TEXT_MAIN)
        self.lbl_java_info.pack(side="left", padx=10, pady=6)

        self.btn_download_java = ctk.CTkButton(
            self.java_badge_frame,
            text=t("installer_java_btn"),
            font=FONT_SMALL,
            width=90,
            height=24,
            fg_color=COLOR_ACCENT_GOLD,
            text_color="#000000",
            hover_color="#f59e0b",
            command=self._download_recommended_java
        )

        # ---------------------------------------------------------------------
        # 4. RAM Bellek Ayarı
        # ---------------------------------------------------------------------
        self.lbl_ram_head = ctk.CTkLabel(left_card, text=t("installer_ram_label"), font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.lbl_ram_head.pack(anchor="w", pady=(2, 2))
        
        ram_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        ram_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(ram_frame, text=t("installer_ram_min"), font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.min_ram_var = ctk.StringVar(value="4")
        self.min_ram_menu = ctk.CTkOptionMenu(ram_frame, variable=self.min_ram_var, values=["1", "2", "4", "6", "8", "12", "16"], width=68, fg_color=COLOR_BG_CARD_HOVER)
        self.min_ram_menu.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(ram_frame, text=t("installer_ram_max"), font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.max_ram_var = ctk.StringVar(value="6")
        self.max_ram_menu = ctk.CTkOptionMenu(ram_frame, variable=self.max_ram_var, values=["2", "4", "6", "8", "10", "12", "16", "24", "32"], width=68, fg_color=COLOR_BG_CARD_HOVER)
        self.max_ram_menu.pack(side="left")

        # ---------------------------------------------------------------------
        # 5. Geyser Bedrock Crossplay Switch
        # ---------------------------------------------------------------------
        self.geyser_switch = ctk.CTkSwitch(
            left_card,
            text=t("installer_crossplay"),
            font=FONT_BOLD,
            text_color=COLOR_ACCENT_GREEN,
            progress_color=COLOR_ACCENT_GREEN
        )
        self.geyser_switch.select()
        self.geyser_switch.pack(anchor="w", pady=(2, 14))

        # ---------------------------------------------------------------------
        # 6. Tek Tıkla Kurulum Butonu
        # ---------------------------------------------------------------------
        self.btn_install = ctk.CTkButton(
            left_card,
            text=t("installer_btn_install"),
            font=FONT_TITLE,
            fg_color=COLOR_ACCENT_CYAN,
            text_color="#000000",
            hover_color="#38bdf8",
            height=44,
            corner_radius=8,
            command=self.start_installation
        )
        self.btn_install.pack(fill="x", pady=(0, 10))

        # ---------------------------------------------------------------------
        # 7. Başlat & Durdur Butonları
        # ---------------------------------------------------------------------
        ctrl_frame = ctk.CTkFrame(left_card, fg_color="transparent")
        ctrl_frame.pack(fill="x", pady=(0, 8))

        self.btn_start = ctk.CTkButton(
            ctrl_frame,
            text=t("installer_btn_start"),
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            hover_color="#34d399",
            height=40,
            corner_radius=8,
            command=self.start_server
        )
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_stop = ctk.CTkButton(
            ctrl_frame,
            text=t("installer_btn_stop"),
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_RED,
            text_color="#ffffff",
            hover_color="#dc2626",
            height=40,
            corner_radius=8,
            command=self.stop_server
        )
        self.btn_stop.pack(side="right", fill="x", expand=True, padx=(4, 0))

        # =====================================================================
        # SAĞ KART: macOS/Linux Stili Terminal & Canlı Konsol
        # =====================================================================
        right_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        right_card.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        right_card.grid_columnconfigure(0, weight=1)
        right_card.grid_rowconfigure(2, weight=1)

        # Terminal Pencere Başlığı
        term_header = ctk.CTkFrame(right_card, fg_color="#0a0f1d", corner_radius=8)
        term_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))

        # Pencere Noktaları (Kırmızı, Sarı, Yeşil)
        dots_frame = ctk.CTkFrame(term_header, fg_color="transparent")
        dots_frame.pack(side="left", padx=10, pady=8)

        ctk.CTkLabel(dots_frame, text="●", font=("Segoe UI", 12), text_color="#ef4444").pack(side="left", padx=2)
        ctk.CTkLabel(dots_frame, text="●", font=("Segoe UI", 12), text_color="#f59e0b").pack(side="left", padx=2)
        ctk.CTkLabel(dots_frame, text="●", font=("Segoe UI", 12), text_color="#10b981").pack(side="left", padx=2)

        ctk.CTkLabel(term_header, text="auto-minecraft-server-maker", font=FONT_CODE, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=6)

        # Sağ Aksiyonlar: AI Çökme Doktoru & Temizle
        btn_clear = ctk.CTkButton(
            term_header,
            text=t("installer_terminal_clear"),
            font=FONT_SMALL,
            width=60,
            height=24,
            fg_color=COLOR_BG_CARD_HOVER,
            hover_color=COLOR_BORDER,
            command=lambda: self.console.delete("1.0", "end")
        )
        btn_clear.pack(side="right", padx=(6, 8))

        btn_ai_doctor = ctk.CTkButton(
            term_header,
            text=t("installer_terminal_doctor"),
            font=FONT_SMALL,
            width=140,
            height=24,
            fg_color=COLOR_ACCENT_PURPLE,
            hover_color="#9333ea",
            command=self._run_ai_doctor
        )
        btn_ai_doctor.pack(side="right", padx=6)

        # İlerleme Çubuğu (Progress Bar)
        self.progress_bar = ctk.CTkProgressBar(right_card, height=4, progress_color=COLOR_ACCENT_CYAN, fg_color="#1e293b")
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        self.progress_bar.set(0)

        # Terminal Metin Alanı
        self.console = ctk.CTkTextbox(
            right_card,
            fg_color="#030712",
            text_color="#38bdf8",
            font=FONT_CODE,
            corner_radius=8,
            border_width=1,
            border_color="#1e293b"
        )
        self.console.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 10))

        # Alt Durum Çubuğu & Canlı Yeşil Rozet
        status_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        status_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))

        self.lbl_server_status = ctk.CTkLabel(
            status_frame,
            text=t("installer_status_stopped"),
            font=FONT_BOLD,
            text_color=COLOR_TEXT_MUTED
        )
        self.lbl_server_status.pack(side="left")

        self.lbl_quick_ip = ctk.CTkLabel(
            status_frame,
            text="IP: 127.0.0.1:25565",
            font=FONT_CODE,
            text_color=COLOR_ACCENT_GREEN
        )
        self.lbl_quick_ip.pack(side="right")

    def _filter_version_category(self, cat_key):
        if cat_key == "all":
            v_list = ServerInstaller.get_supported_versions()
        else:
            v_list = ServerInstaller.get_supported_versions(cat_key)
        self.ver_menu.configure(values=v_list)
        if v_list:
            self.ver_var.set(v_list[0])
            self._update_java_status()

    def _on_custom_ver_changed(self, event=None):
        val = self.custom_ver_var.get().strip()
        if val:
            self.ver_var.set(val)
            self._update_java_status()

    def _select_flavor(self, full_name, short_name):
        self.flavor_var.set(full_name)
        for s_name, btn in self.flavor_pills.items():
            if s_name == short_name:
                btn.configure(fg_color=COLOR_ACCENT_CYAN, text_color="#000000")
            else:
                btn.configure(fg_color=COLOR_BG_CARD_HOVER, text_color=COLOR_TEXT_MAIN)

    def _update_java_status(self):
        try:
            raw_ver = self.ver_var.get()
            mc_ver = ServerInstaller.get_clean_version(raw_ver)
            rec_j = JavaDetector.get_recommended_java_version(mc_ver)
            sys_j = JavaDetector.get_system_java()

            if not sys_j or sys_j.get('version', 0) <= 0:
                self.lbl_java_info.configure(text=f"⚠️ Java bulunamadı! (Önerilen: Java {rec_j})", text_color=COLOR_ACCENT_RED)
                self.btn_download_java.pack(side="right", padx=10, pady=4)
            elif sys_j['version'] < rec_j:
                self.lbl_java_info.configure(
                    text=f"⚠️ Sistemde Java {sys_j['version']} var, {mc_ver} için Java {rec_j} gerekli!",
                    text_color=COLOR_ACCENT_GOLD
                )
                self.btn_download_java.pack(side="right", padx=10, pady=4)
            else:
                self.lbl_java_info.configure(
                    text=f"✔ Uyumlu: Java {sys_j['version']} ({mc_ver} için hazır)",
                    text_color=COLOR_ACCENT_GREEN
                )
                self.btn_download_java.pack_forget()
        except Exception as e:
            self.lbl_java_info.configure(text=f"Java durumu: {e}", text_color=COLOR_TEXT_MUTED)

    def _download_recommended_java(self):
        mc_ver = self.ver_var.get()
        rec_j = JavaDetector.get_recommended_java_version(mc_ver)
        self.log(f"> Java {rec_j} indirme sayfası açılıyor...")
        JavaDetector.open_java_download_page(rec_j)

    def _apply_and_run_ai_chip(self, prompt_text):
        self.ai_prompt_var.set(prompt_text)
        self._run_ai_wizard()

    def _run_ai_wizard(self):
        prompt = self.ai_prompt_var.get().strip()
        if not prompt:
            prompt = "Arkadaşlarımla 1.20.4 hafif Paper kur"

        self.log(f"\n=======================================================")
        self.log(f"🤖 [AI OTONOM KURULUM BAŞLATILDI]: '{prompt}'")
        self.log(f"=======================================================")

        # Run parser
        plan = self.ai_engineer.parse_setup_intent(prompt)
        self.last_ai_plan = plan

        # Update UI Controls to match AI Plan
        self.ver_var.set(plan["mc_version"])
        self.min_ram_var.set(str(plan["min_ram"]))
        self.max_ram_var.set(str(plan["max_ram"]))
        if plan["install_geyser"]:
            self.geyser_switch.select()
        else:
            self.geyser_switch.deselect()

        # Update flavor pill
        matched_flavor = plan["server_type"]
        for sn in self.flavor_pills:
            if sn.lower() in matched_flavor.lower():
                self._select_flavor(f"{sn} (AI Önerisi)", sn)
                break

        self.log(f"> AI Kararı: Sürüm {plan['mc_version']} | Tür: {plan['server_type']}")
        self.log(f"> RAM: {plan['min_ram']}GB - {plan['max_ram']}GB | Crossplay: {plan['install_geyser']}")
        self.log(f"> {plan['explanation']}\n")

        # Automatically start installation
        self.start_installation()

    def log(self, text):
        self.console.insert("end", f"{text}\n")
        self.console.see("end")

    def _progress_callback(self, percent, *args, **kwargs):
        try:
            val = float(percent) / 100.0
            self.after(0, lambda: self.progress_bar.set(max(0.0, min(1.0, val))))
        except Exception:
            pass

    def start_installation(self):
        s_cfg = self.config_manager.get_server_config()
        server_dir = s_cfg.get("server_dir", "./server")
        raw_flavor = self.flavor_var.get().split()[0].replace("(", "").replace(")", "").strip()
        mc_ver = ServerInstaller.get_clean_version(self.ver_var.get())
        min_ram = int(self.min_ram_var.get())
        max_ram = int(self.max_ram_var.get())
        geyser_val = bool(self.geyser_switch.get())

        self.btn_install.configure(state="disabled", text="⏳ İndiriliyor & Yapılandırılıyor...")
        self.progress_bar.set(0.1)

        def _worker():
            try:
                installer = ServerInstaller(
                    server_dir,
                    log_callback=self.log,
                    progress_callback=self._progress_callback
                )
                success = installer.setup_server(
                    server_type=raw_flavor,
                    mc_version=mc_ver,
                    min_ram=min_ram,
                    max_ram=max_ram,
                    rcon_port=s_cfg.get("rcon_port", 25575),
                    rcon_pass=s_cfg.get("rcon_password", "admin123"),
                    server_port=s_cfg.get("port", 25565),
                    install_geyser=geyser_val
                )

                # Autonomous Safe Mod Installation via Modrinth
                is_modded = raw_flavor in ["Forge", "Fabric", "NeoForge", "Arclight", "Mohist"] or getattr(self, "last_ai_plan", {}).get("is_modded", False)
                if success and is_modded:
                    try:
                        self.log("\n=======================================================")
                        self.log("📦 [AI OTONOM MOD YÖNETİCİSİ]: Uyumlu Modlar Yükleniyor...")
                        self.log("=======================================================")
                        from core.mod_fetcher import ModFetcher
                        fetcher = ModFetcher(log_callback=self.log)
                        prompt_to_use = getattr(self, "last_ai_plan", {}).get("raw_prompt", self.ai_prompt_var.get())
                        mods_dir = os.path.join(server_dir, "mods")
                        fetcher.auto_install_theme_mods(
                            prompt=prompt_to_use,
                            mc_version=mc_ver,
                            loader=raw_flavor,
                            mods_dir=mods_dir
                        )
                    except Exception as mod_err:
                        self.log(f"Mod indirme uyarısı (sunucu kurulumu etkilendi): {mod_err}")

                self.progress_bar.set(1.0 if success else 0)
            except Exception as e:
                self.log(f"Kritik Kurulum Hatası: {e}")
            finally:
                self.after(0, lambda: self.btn_install.configure(state="normal", text=t("installer_btn_install")))

        threading.Thread(target=_worker, daemon=True).start()

    def start_server(self):
        s_cfg = self.config_manager.get_server_config()
        server_dir = os.path.abspath(s_cfg.get("server_dir", "./server"))
        start_bat = os.path.join(server_dir, "start.bat")

        if not os.path.exists(start_bat):
            messagebox.showwarning("Eksik Dosya", "start.bat bulunamadı. Lütfen önce 'TEK TIKLA İNDİR & KUR' butonuna basınız.")
            return

        self.log(f"> Sunucu başlatılıyor: {start_bat}")
        try:
            self.server_process = subprocess.Popen(
                ["cmd.exe", "/c", start_bat],
                cwd=server_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.lbl_server_status.configure(text=t("installer_status_starting"), text_color=COLOR_ACCENT_GOLD)
        except Exception as e:
            self.log(f"Sunucu başlatılamadı: {e}")

    def stop_server(self):
        self.log("> Sunucu durdurma sinyali gönderiliyor...")
        try:
            from core.rcon_client import MinecraftRcon
            s_cfg = self.config_manager.get_server_config()
            rcon = MinecraftRcon(port=s_cfg.get("rcon_port", 25575), password=s_cfg.get("rcon_password", "admin123"))
            resp = rcon.send_command("stop")
            self.log(f"> RCON Yanıtı: {resp}")
        except Exception:
            pass

        if self.server_process:
            try:
                self.server_process.terminate()
            except Exception:
                pass
            self.server_process = None

        self.lbl_server_status.configure(text=t("installer_status_stopped"), text_color=COLOR_TEXT_MUTED)

    def _start_server_watcher(self):
        def _watch():
            while True:
                time.sleep(2.5)
                s_cfg = self.config_manager.get_server_config()
                port = s_cfg.get("port", 25565)
                is_up = False
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.8)
                    if s.connect_ex(("127.0.0.1", port)) == 0:
                        is_up = True
                    s.close()
                except Exception:
                    pass

                def _ui():
                    if is_up:
                        self.lbl_server_status.configure(
                            text=t("installer_status_running"),
                            text_color=COLOR_ACCENT_GREEN
                        )
                    elif self.server_process:
                        self.lbl_server_status.configure(
                            text=t("installer_status_starting"),
                            text_color=COLOR_ACCENT_GOLD
                        )
                    else:
                        self.lbl_server_status.configure(
                            text=t("installer_status_stopped"),
                            text_color=COLOR_TEXT_MUTED
                        )
                self.after(0, _ui)

        threading.Thread(target=_watch, daemon=True).start()

    def _run_ai_doctor(self):
        console_txt = self.console.get("1.0", "end").strip()
        if not console_txt:
            messagebox.showinfo("AI Çökme Doktoru", "Konsolda analiz edilecek bir hata kaydı bulunmuyor.")
            return

        self.log("\n🩺 [AI ÇÖKME DOKTORU DEVREYE GİRDİ]: Konsol günlüğü taranıyor...")
        def _doc():
            ai = AIEngineer(self.config_manager)
            res = ai.analyze_log_error(console_txt[-2000:])
            self.after(0, lambda: self.log(f"\n💡 [AI REÇETESİ & ÇÖZÜM]:\n{res}\n"))
        threading.Thread(target=_doc, daemon=True).start()

    def _filter_version_category(self, cat_key):
        if cat_key == "all":
            vers = ServerInstaller.SUPPORTED_VERSIONS
        else:
            vers = ServerInstaller.get_supported_versions(cat_key)

        self.ver_menu.configure(values=vers)
        if vers:
            self.ver_var.set(vers[0])
            self._update_java_status()

