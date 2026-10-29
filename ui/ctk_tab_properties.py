# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: Visual server.properties Editor (v3.9.0 Ultimate)
Allows configuring core Minecraft server behaviors with switches, dropdowns, and sliders:
- MOTD, Port, Max Players, Game Mode, Difficulty
- Online-mode (Premium/Cracked free account switch)
- PvP, Hardcore, Flight, Command Blocks, Whitelist
- View Distance, Simulation Distance, Spawn Protection, Mob Spawning
"""

import os
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.properties_manager import PropertiesManager

class CTkTabProperties(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        sdir = self.config_manager.get_server_config().get("server_dir", os.path.join(os.getcwd(), "server"))
        self.prop_mgr = PropertiesManager(sdir)

        self._build_ui()
        self._load_values()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        scroll_card = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        scroll_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Başlık Banner
        header = ctk.CTkFrame(scroll_card, fg_color="#0a0f1d", corner_radius=10, border_width=1, border_color=COLOR_ACCENT_GOLD)
        header.pack(fill="x", padx=16, pady=(12, 14))

        h_in = ctk.CTkFrame(header, fg_color="transparent")
        h_in.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(h_in, text="⚙️ GÖRSEL SERVER.PROPERTIES AYAR MERKEZİ", font=FONT_TITLE, text_color=COLOR_ACCENT_GOLD).pack(anchor="w")
        ctk.CTkLabel(h_in, text="Sunucu portu, oyun modu, korsan/orijinal girişi, zorluk ve performans ayarlarını tek tıkla düzenleyin.", font=FONT_REGULAR, text_color=COLOR_TEXT_MAIN).pack(anchor="w")

        # 1. MOTD
        ctk.CTkLabel(scroll_card, text="📝 Sunucu Başlığı (MOTD - Çok Oyunculu Listesinde Görünür):", font=FONT_BOLD).pack(anchor="w", padx=16, pady=(4, 2))
        self.motd_var = ctk.StringVar()
        self.motd_entry = ctk.CTkEntry(scroll_card, textvariable=self.motd_var, font=FONT_REGULAR, height=36, fg_color="#030712")
        self.motd_entry.pack(fill="x", padx=16, pady=(0, 12))

        # 2. Port & Maksimum Oyuncu
        row_net = ctk.CTkFrame(scroll_card, fg_color="transparent")
        row_net.pack(fill="x", padx=16, pady=(0, 12))

        col_port = ctk.CTkFrame(row_net, fg_color="transparent")
        col_port.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(col_port, text="🔌 Sunucu Portu (Varsayılan 25565):", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.port_var = ctk.StringVar(value="25565")
        ctk.CTkEntry(col_port, textvariable=self.port_var, height=32, fg_color="#030712").pack(fill="x")

        col_players = ctk.CTkFrame(row_net, fg_color="transparent")
        col_players.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(col_players, text="👥 Maksimum Oyuncu Kapasitesi:", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.max_p_var = ctk.StringVar(value="20")
        ctk.CTkEntry(col_players, textvariable=self.max_p_var, height=32, fg_color="#030712").pack(fill="x")

        # 3. Oyun Modu & Zorluk
        row1 = ctk.CTkFrame(scroll_card, fg_color="transparent")
        row1.pack(fill="x", padx=16, pady=(0, 12))

        col1 = ctk.CTkFrame(row1, fg_color="transparent")
        col1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(col1, text="🎮 Varsayılan Oyun Modu:", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.gamemode_var = ctk.StringVar(value="survival")
        self.gamemode_menu = ctk.CTkOptionMenu(col1, variable=self.gamemode_var, values=["survival", "creative", "adventure", "spectator"], fg_color=COLOR_BG_CARD_HOVER)
        self.gamemode_menu.pack(fill="x")

        col2 = ctk.CTkFrame(row1, fg_color="transparent")
        col2.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(col2, text="💀 Zorluk Seviyesi:", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.diff_var = ctk.StringVar(value="normal")
        self.diff_menu = ctk.CTkOptionMenu(col2, variable=self.diff_var, values=["peaceful", "easy", "normal", "hard"], fg_color=COLOR_BG_CARD_HOVER)
        self.diff_menu.pack(fill="x")

        # 4. Görüş & Simülasyon Mesafesi & Spawn Koruması
        row2 = ctk.CTkFrame(scroll_card, fg_color="transparent")
        row2.pack(fill="x", padx=16, pady=(0, 14))

        col_view = ctk.CTkFrame(row2, fg_color="transparent")
        col_view.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(col_view, text="👁️ Görüş Mesafesi:", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.view_dist_var = ctk.StringVar(value="10")
        ctk.CTkOptionMenu(col_view, variable=self.view_dist_var, values=["6", "8", "10", "12", "16", "24", "32"], fg_color=COLOR_BG_CARD_HOVER).pack(fill="x")

        col_sim = ctk.CTkFrame(row2, fg_color="transparent")
        col_sim.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(col_sim, text="⚡ Simülasyon Mesafesi:", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.sim_dist_var = ctk.StringVar(value="8")
        ctk.CTkOptionMenu(col_sim, variable=self.sim_dist_var, values=["4", "6", "8", "10", "12"], fg_color=COLOR_BG_CARD_HOVER).pack(fill="x")

        col_spawn = ctk.CTkFrame(row2, fg_color="transparent")
        col_spawn.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(col_spawn, text="🛡️ Spawn Koruması (Blok):", font=FONT_BOLD).pack(anchor="w", pady=(0, 2))
        self.spawn_prot_var = ctk.StringVar(value="16")
        ctk.CTkEntry(col_spawn, textvariable=self.spawn_prot_var, height=28, fg_color="#030712").pack(fill="x")

        # 5. Gelişmiş Anahtarlar & Switchler (Online Mode, PvP, Canavarlar...)
        sw_card = ctk.CTkFrame(scroll_card, fg_color=COLOR_BG_CARD_HOVER, corner_radius=10)
        sw_card.pack(fill="x", padx=16, pady=(0, 16))

        # Online Mode (Korsan/Orijinal Hesap Girişi)
        self.online_mode_sw = ctk.CTkSwitch(
            sw_card,
            text="🔓 Korsan & Ücretsiz Launcher Girişine İzin Ver (online-mode=false)",
            font=FONT_BOLD,
            text_color=COLOR_ACCENT_GREEN
        )
        self.online_mode_sw.pack(anchor="w", padx=14, pady=8)

        self.pvp_sw = ctk.CTkSwitch(sw_card, text="⚔️ Oyuncular Arası Hasar (PvP)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.pvp_sw.pack(anchor="w", padx=14, pady=8)

        self.hardcore_sw = ctk.CTkSwitch(sw_card, text="💀 Hardcore Modu (Ölen İzleyici Olur)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.hardcore_sw.pack(anchor="w", padx=14, pady=8)

        self.cmd_block_sw = ctk.CTkSwitch(sw_card, text="🧱 Komut Blokları Aktif (enable-command-block)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.cmd_block_sw.pack(anchor="w", padx=14, pady=8)

        self.flight_sw = ctk.CTkSwitch(sw_card, text="🕊️ Uçuş İzni (allow-flight)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.flight_sw.pack(anchor="w", padx=14, pady=8)

        self.monsters_sw = ctk.CTkSwitch(sw_card, text="👾 Canavarlar Doğsun (spawn-monsters)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.monsters_sw.pack(anchor="w", padx=14, pady=8)

        self.animals_sw = ctk.CTkSwitch(sw_card, text="🐷 Hayvanlar Doğsun (spawn-animals)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.animals_sw.pack(anchor="w", padx=14, pady=8)

        self.wl_sw = ctk.CTkSwitch(sw_card, text="🛡️ Beyaz Liste (Whitelist - Yalnızca İzinli Oyuncular)", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN)
        self.wl_sw.pack(anchor="w", padx=14, pady=8)

        # 6. Kaydet Butonu
        btn_save = ctk.CTkButton(
            scroll_card,
            text="💾 TÜM AYARLARI SERVER.PROPERTIES'E KAYDET",
            font=FONT_TITLE,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            hover_color="#34d399",
            height=44,
            corner_radius=8,
            command=self._save_values
        )
        btn_save.pack(fill="x", padx=16, pady=(4, 16))

    def _load_values(self):
        props = self.prop_mgr.read_properties()
        self.motd_var.set(props.get("motd", "Auto Minecraft Server"))
        self.port_var.set(props.get("server-port", "25565"))
        self.gamemode_var.set(props.get("gamemode", "survival"))
        self.diff_var.set(props.get("difficulty", "normal"))
        self.max_p_var.set(props.get("max-players", "20"))
        self.view_dist_var.set(props.get("view-distance", "10"))
        self.sim_dist_var.set(props.get("simulation-distance", "8"))
        self.spawn_prot_var.set(props.get("spawn-protection", "16"))

        # online-mode: false ise switch AÇIK (korsan girişine izin verildi)
        if props.get("online-mode", "true").lower() == "false":
            self.online_mode_sw.select()
        else:
            self.online_mode_sw.deselect()

        if props.get("pvp", "true") == "true": self.pvp_sw.select()
        else: self.pvp_sw.deselect()

        if props.get("hardcore", "false") == "true": self.hardcore_sw.select()
        else: self.hardcore_sw.deselect()

        if props.get("enable-command-block", "true") == "true": self.cmd_block_sw.select()
        else: self.cmd_block_sw.deselect()

        if props.get("allow-flight", "true") == "true": self.flight_sw.select()
        else: self.flight_sw.deselect()

        if props.get("spawn-monsters", "true") == "true": self.monsters_sw.select()
        else: self.monsters_sw.deselect()

        if props.get("spawn-animals", "true") == "true": self.animals_sw.select()
        else: self.animals_sw.deselect()

        if props.get("white-list", "false") == "true": self.wl_sw.select()
        else: self.wl_sw.deselect()

    def _save_values(self):
        allow_cracked = (self.online_mode_sw.get() == 1)
        online_mode_val = "false" if allow_cracked else "true"

        new_props = {
            "motd": self.motd_var.get().strip(),
            "server-port": self.port_var.get().strip() or "25565",
            "gamemode": self.gamemode_var.get(),
            "difficulty": self.diff_var.get(),
            "max-players": self.max_p_var.get().strip(),
            "view-distance": self.view_dist_var.get(),
            "simulation-distance": self.sim_dist_var.get(),
            "spawn-protection": self.spawn_prot_var.get().strip(),
            "online-mode": online_mode_val,
            "pvp": "true" if self.pvp_sw.get() == 1 else "false",
            "hardcore": "true" if self.hardcore_sw.get() == 1 else "false",
            "enable-command-block": "true" if self.cmd_block_sw.get() == 1 else "false",
            "allow-flight": "true" if self.flight_sw.get() == 1 else "false",
            "spawn-monsters": "true" if self.monsters_sw.get() == 1 else "false",
            "spawn-animals": "true" if self.animals_sw.get() == 1 else "false",
            "white-list": "true" if self.wl_sw.get() == 1 else "false"
        }
        ok = self.prop_mgr.save_properties(new_props)
        if ok:
            messagebox.showinfo("Başarılı", "✅ server.properties ayarları başarıyla kaydedildi!")
        else:
            messagebox.showerror("Hata", "server.properties kaydedilirken hata oluştu.")
