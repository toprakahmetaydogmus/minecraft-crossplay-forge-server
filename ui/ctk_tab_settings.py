# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: Settings & 12-Provider API Key Vault
100% Zero-Leak Security: Keys are stored exclusively in local config.json.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.ai_engineer import AIEngineer

class CTkTabSettings(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        self.ai = AIEngineer(config_manager)

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        scroll_card = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        scroll_card.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # 1. AI API ANAHTARLARI KASASI
        ctk.CTkLabel(scroll_card, text="🤖 AI SAĞLAYICILARI & API KASASI (12 FARKLI MOTOR)", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_CYAN).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(scroll_card, text="🔒 100% Zero-Leak Güvenlik: Anahtarlarınız kesinlikle internete veya GitHub'a gitmez, yalnızca bilgisayarınızdaki izole config.json'da saklanır.", font=FONT_SMALL, text_color=COLOR_ACCENT_GREEN).pack(anchor="w", padx=16, pady=(0, 12))

        ai_cfg = self.config_manager.get_ai_config()
        providers = ai_cfg.get("providers", {})

        self.key_entries = {}
        for pname, pinfo in providers.items():
            row = ctk.CTkFrame(scroll_card, fg_color=COLOR_BG_CARD_HOVER, corner_radius=8)
            row.pack(fill="x", padx=16, pady=3)

            lbl = ctk.CTkLabel(row, text=f"{pname}:", font=FONT_BOLD, width=170, anchor="w", text_color=COLOR_TEXT_MAIN)
            lbl.pack(side="left", padx=(12, 6), pady=6)

            k_var = ctk.StringVar(value=pinfo.get("api_key", ""))
            show_ch = "" if "Ollama" in pname else "•"
            ent = ctk.CTkEntry(row, textvariable=k_var, show=show_ch, font=FONT_CODE, fg_color="#030712", height=32)
            ent.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=6)
            self.key_entries[pname] = k_var

            btn_test = ctk.CTkButton(
                row,
                text="Test Et",
                font=FONT_SMALL,
                width=70,
                height=30,
                fg_color=COLOR_ACCENT_CYAN,
                text_color="#000000",
                command=lambda pn=pname: self.test_provider(pn)
            )
            btn_test.pack(side="right", padx=10, pady=6)

        # 2. SUNUCU & RCON AYARLARI
        ctk.CTkLabel(scroll_card, text="⚙️ SUNUCU & RCON BAĞLANTI AYARLARI", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_GOLD).pack(anchor="w", padx=16, pady=(16, 4))

        srv_cfg = self.config_manager.get_server_config()
        s_box = ctk.CTkFrame(scroll_card, fg_color=COLOR_BG_CARD_HOVER, corner_radius=8)
        s_box.pack(fill="x", padx=16, pady=(0, 16))

        r1 = ctk.CTkFrame(s_box, fg_color="transparent")
        r1.pack(fill="x", padx=12, pady=6)
        ctk.CTkLabel(r1, text="RCON Host:", font=FONT_BOLD, width=120, anchor="w").pack(side="left")
        self.rcon_host_var = ctk.StringVar(value=srv_cfg.get("rcon_host", "127.0.0.1"))
        ctk.CTkEntry(r1, textvariable=self.rcon_host_var, width=160, fg_color="#030712").pack(side="left", padx=(0, 16))

        ctk.CTkLabel(r1, text="RCON Port:", font=FONT_BOLD, width=90, anchor="w").pack(side="left")
        self.rcon_port_var = ctk.StringVar(value=str(srv_cfg.get("rcon_port", 25575)))
        ctk.CTkEntry(r1, textvariable=self.rcon_port_var, width=90, fg_color="#030712").pack(side="left")

        r2 = ctk.CTkFrame(s_box, fg_color="transparent")
        r2.pack(fill="x", padx=12, pady=6)
        ctk.CTkLabel(r2, text="RCON Şifresi:", font=FONT_BOLD, width=120, anchor="w").pack(side="left")
        self.rcon_pass_var = ctk.StringVar(value=srv_cfg.get("rcon_password", "admin123"))
        ctk.CTkEntry(r2, textvariable=self.rcon_pass_var, show="•", width=160, fg_color="#030712").pack(side="left", padx=(0, 16))

        ctk.CTkLabel(r2, text="Java Port:", font=FONT_BOLD, width=90, anchor="w").pack(side="left")
        self.srv_port_var = ctk.StringVar(value=str(srv_cfg.get("server_port", 25565)))
        ctk.CTkEntry(r2, textvariable=self.srv_port_var, width=90, fg_color="#030712").pack(side="left")

        # 3. KAYDET BUTONU
        btn_save = ctk.CTkButton(
            scroll_card,
            text="💾 TÜM AYARLARI GÜVENLİ KAYDET",
            font=FONT_TITLE,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            hover_color="#34d399",
            height=42,
            corner_radius=8,
            command=self.save_settings
        )
        btn_save.pack(fill="x", padx=16, pady=(6, 20))

    def test_provider(self, provider_name):
        key = self.key_entries[provider_name].get().strip()

        if "Ollama" in provider_name:
            from core.local_ai_manager import LocalAIManager
            mgr = LocalAIManager()
            if not mgr.is_service_running():
                if messagebox.askyesno("Ollama Servisi", "Ollama arka plan servisi kapalı görünüyor. Otomatik başlatılsın mı?"):
                    mgr.ensure_service_running()
            st = mgr.get_status()
            if st.get("running"):
                messagebox.showinfo("Ollama Başarılı", f"✅ Ollama Yerel Servisi Aktif!\nYüklü Modeller: {', '.join(st.get('models', [])) or 'Yok'}\n\n100% Çevrimdışı ve Ücretsiz!")
            else:
                messagebox.showerror("Ollama Hatası", "Ollama servisi çalışmıyor. 'AI Sunucu Mühendisi' sekmesinden 'İndir & Kur' yapabilirsiniz.")
            return

        messagebox.showinfo("Bağlantı Testi", f"[*] {provider_name} servisine ping atılıyor...")
        def _worker():
            resp = self.ai.ask("Ping! Bu bir bağlantı testidir, tek kelime 'OK' yanıtı ver.", provider_name=provider_name, api_key=key)
            if "Hatası" in resp or "Hata" in resp:
                self.after(0, messagebox.showerror, "Test Başarısız", f"{provider_name} Yanıtı:\n{resp}")
            else:
                self.after(0, messagebox.showinfo, "Test Başarılı", f"✅ {provider_name} başarıyla yanıt verdi:\n\n{resp}")
        threading.Thread(target=_worker, daemon=True).start()

    def save_settings(self):
        cfg = self.config_manager.config
        for pname, var in self.key_entries.items():
            if pname in cfg["ai"]["providers"]:
                cfg["ai"]["providers"][pname]["api_key"] = var.get().strip()

        try:
            cfg["server"]["rcon_host"] = self.rcon_host_var.get().strip()
            cfg["server"]["rcon_port"] = int(self.rcon_port_var.get().strip())
            cfg["server"]["rcon_password"] = self.rcon_pass_var.get().strip()
            cfg["server"]["server_port"] = int(self.srv_port_var.get().strip())
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz port: {e}")
            return

        ok = self.config_manager.save(cfg)
        if ok:
            messagebox.showinfo("Kaydedildi", "✅ Tüm ayarlar başarıyla yerel config.json kasasına kaydedildi.")
        else:
            messagebox.showerror("Hata", "Ayarlar kaydedilemedi.")
