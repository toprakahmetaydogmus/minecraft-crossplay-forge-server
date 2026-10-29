# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: 1-Click Plugin & Mod Hub
Browse, install, and manage 12+ essential high-performance plugins with 1 click.
"""

import os
import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.plugin_mod_hub import PluginModHub, POPULAR_PLUGINS

class CTkTabPlugins(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        sdir = self.config_manager.get_server_config().get("server_dir", os.path.join(os.getcwd(), "server"))
        self.hub = PluginModHub(sdir, log_callback=self._on_log)

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Üst Başlık & Bilgi
        header_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        header_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))

        h_inner = ctk.CTkFrame(header_card, fg_color="transparent")
        h_inner.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(h_inner, text="🔌 1-TIKLA EKLENTİ (PLUGIN) VE MOD MERKEZİ", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_GREEN).pack(side="left")

        btn_refresh = ctk.CTkButton(
            h_inner,
            text="🔄 Yenile",
            font=FONT_SMALL,
            width=80,
            height=28,
            fg_color=COLOR_BG_CARD_HOVER,
            command=self._refresh_list
        )
        btn_refresh.pack(side="right")

        # Scrollable Eklenti Listesi
        self.scroll_list = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        self.scroll_list.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self._render_plugin_cards()

    def _render_plugin_cards(self):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        installed = self.hub.get_installed_plugins()

        for p in POPULAR_PLUGINS:
            row = ctk.CTkFrame(self.scroll_list, fg_color=COLOR_BG_CARD_HOVER, corner_radius=8)
            row.pack(fill="x", padx=8, pady=4)

            # Sol Bilgi
            info_f = ctk.CTkFrame(row, fg_color="transparent")
            info_f.pack(side="left", fill="both", expand=True, padx=12, pady=8)

            head_row = ctk.CTkFrame(info_f, fg_color="transparent")
            head_row.pack(fill="x")

            ctk.CTkLabel(head_row, text=p["name"], font=FONT_BOLD, text_color=COLOR_ACCENT_CYAN).pack(side="left", padx=(0, 8))
            ctk.CTkLabel(head_row, text=f"[{p['category']}]", font=FONT_SMALL, text_color=COLOR_ACCENT_GOLD).pack(side="left")

            ctk.CTkLabel(info_f, text=p["desc"], font=FONT_SMALL, text_color=COLOR_TEXT_MUTED, justify="left").pack(anchor="w", pady=(2, 0))

            # Sağ Durum & Kurulum Butonu
            is_inst = any(p["filename"].lower() in f.lower() for f in installed)
            if is_inst:
                lbl_inst = ctk.CTkLabel(row, text="✅ Yüklü", font=FONT_BOLD, text_color=COLOR_ACCENT_GREEN, width=90)
                lbl_inst.pack(side="right", padx=12)
            else:
                btn_install = ctk.CTkButton(
                    row,
                    text="📥 Kur",
                    font=FONT_BOLD,
                    width=90,
                    height=30,
                    fg_color=COLOR_ACCENT_GREEN,
                    text_color="#000000",
                    hover_color="#34d399",
                    command=lambda plug=p: self._install_plugin(plug)
                )
                btn_install.pack(side="right", padx=12)

    def _install_plugin(self, plug):
        def _worker():
            ok = self.hub.install_plugin(plug)
            self.after(0, self._render_plugin_cards)
            if ok:
                self.after(0, messagebox.showinfo, "Eklenti Kuruldu", f"✅ '{plug['name']}' başarıyla plugins klasörüne kuruldu!")
            else:
                self.after(0, messagebox.showerror, "Hata", f"❌ '{plug['name']}' indirilirken bir sorun oluştu.")
        threading.Thread(target=_worker, daemon=True).start()

    def _refresh_list(self):
        sdir = self.config_manager.get_server_config().get("server_dir", os.path.join(os.getcwd(), "server"))
        self.hub = PluginModHub(sdir, log_callback=self._on_log)
        self._render_plugin_cards()

    def _on_log(self, msg):
        pass
