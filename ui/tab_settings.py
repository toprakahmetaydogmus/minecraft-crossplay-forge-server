# -*- coding: utf-8 -*-
"""
Tab: Settings & 12-Provider API Key Vault
100% Zero-Leak: API Keys are stored strictly in local, gitignored config.json.
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import *
from core.ai_engineer import AIEngineer

class TabSettings:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.frame = tk.Frame(parent, bg=BG_DARK)
        self.ai = AIEngineer(config_manager)

        self._build_ui()

    def _build_ui(self):
        canvas = tk.Canvas(self.frame, bg=BG_DARK, highlightthickness=0, borderwidth=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg=BG_DARK)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=14, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # 1. AI API ANAHTARLARI KASASI (12 SAĞLAYICI)
        sec_ai = tk.LabelFrame(scroll_content, text=" 🤖 AI SAĞLAYICILARI & API ANAHTARI KASASI (12 Motor) ", font=("Segoe UI", 10, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL, padx=14, pady=12)
        sec_ai.pack(fill=tk.X, pady=(0, 14))

        info_lbl = tk.Label(
            sec_ai,
            text="🔒 100% Zero-Leak Güvenlik: Anahtarlarınız asla GitHub'a gitmez, yalnızca yerel config.json dosyanızda şifreli/izole saklanır.",
            font=("Segoe UI", 8, "italic"),
            fg=ACCENT_GREEN,
            bg=BG_PANEL
        )
        info_lbl.pack(anchor="w", pady=(0, 10))

        ai_cfg = self.config_manager.get_ai_config()
        providers = ai_cfg.get("providers", {})

        self.key_entries = {}
        for idx, (pname, pinfo) in enumerate(providers.items()):
            row = tk.Frame(sec_ai, bg=BG_PANEL)
            row.pack(fill=tk.X, pady=3)

            lbl = tk.Label(row, text=f"{pname}:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=22, anchor="w")
            lbl.pack(side=tk.LEFT)

            key_var = tk.StringVar(value=pinfo.get("api_key", ""))
            show_char = "" if "Ollama" in pname else "•"
            ent = tk.Entry(row, textvariable=key_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", insertbackground=ACCENT_CYAN, show=show_char, relief=tk.FLAT, width=42)
            ent.pack(side=tk.LEFT, padx=(0, 8), ipady=2)
            self.key_entries[pname] = key_var

            btn_test = tk.Button(row, text="Bağlantı Testi", font=("Segoe UI", 8), bg=BG_CARD, fg=ACCENT_CYAN, relief=tk.FLAT, padx=6, command=lambda pn=pname: self.test_provider(pn))
            btn_test.pack(side=tk.LEFT)

        # 2. SUNUCU & RCON AYARLARI
        sec_srv = tk.LabelFrame(scroll_content, text=" ⚙️ SUNUCU & RCON BAĞLANTI AYARLARI ", font=("Segoe UI", 10, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL, padx=14, pady=12)
        sec_srv.pack(fill=tk.X, pady=(0, 14))

        srv_cfg = self.config_manager.get_server_config()

        row_s1 = tk.Frame(sec_srv, bg=BG_PANEL)
        row_s1.pack(fill=tk.X, pady=3)
        tk.Label(row_s1, text="RCON Host:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=16, anchor="w").pack(side=tk.LEFT)
        self.rcon_host_var = tk.StringVar(value=srv_cfg.get("rcon_host", "127.0.0.1"))
        tk.Entry(row_s1, textvariable=self.rcon_host_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", width=18, relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 14), ipady=2)

        tk.Label(row_s1, text="RCON Port:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=12, anchor="w").pack(side=tk.LEFT)
        self.rcon_port_var = tk.StringVar(value=str(srv_cfg.get("rcon_port", 25575)))
        tk.Entry(row_s1, textvariable=self.rcon_port_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", width=8, relief=tk.FLAT).pack(side=tk.LEFT, ipady=2)

        row_s2 = tk.Frame(sec_srv, bg=BG_PANEL)
        row_s2.pack(fill=tk.X, pady=3)
        tk.Label(row_s2, text="RCON Şifresi:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=16, anchor="w").pack(side=tk.LEFT)
        self.rcon_pass_var = tk.StringVar(value=srv_cfg.get("rcon_password", "admin123"))
        tk.Entry(row_s2, textvariable=self.rcon_pass_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", width=24, relief=tk.FLAT, show="•").pack(side=tk.LEFT, padx=(0, 14), ipady=2)

        row_s3 = tk.Frame(sec_srv, bg=BG_PANEL)
        row_s3.pack(fill=tk.X, pady=3)
        tk.Label(row_s3, text="Oyun Portu (Java):", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=16, anchor="w").pack(side=tk.LEFT)
        self.srv_port_var = tk.StringVar(value=str(srv_cfg.get("server_port", 25565)))
        tk.Entry(row_s3, textvariable=self.srv_port_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", width=8, relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 14), ipady=2)

        tk.Label(row_s3, text="Bedrock Portu:", font=("Segoe UI", 9, "bold"), fg=TEXT_COLOR, bg=BG_PANEL, width=14, anchor="w").pack(side=tk.LEFT)
        self.bedrock_port_var = tk.StringVar(value=str(srv_cfg.get("bedrock_port", 19132)))
        tk.Entry(row_s3, textvariable=self.bedrock_port_var, font=("Consolas", 9), bg=BG_CARD, fg="#ffffff", width=8, relief=tk.FLAT).pack(side=tk.LEFT, ipady=2)

        # 3. KAYDET BUTONU
        btn_save = tk.Button(
            scroll_content,
            text="💾 TÜM AYARLARI GÜVENLİ KAYDET",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_GREEN,
            fg="#000000",
            activebackground="#059669",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.save_settings
        )
        btn_save.pack(anchor="w", pady=(8, 20))

    def test_provider(self, provider_name):
        key = self.key_entries[provider_name].get().strip()

        if "Ollama" in provider_name:
            from core.local_ai_manager import LocalAIManager
            mgr = LocalAIManager()
            if not mgr.is_service_running():
                if messagebox.askyesno("Ollama Servisi Kapalı", "Ollama arka plan servisi (127.0.0.1:11434) şu anda kapalı görünüyor.\n\nServisi otomatik başlatmak ister misiniz?"):
                    mgr.ensure_service_running()
            status = mgr.get_status()
            models_txt = ", ".join(status.get("models", [])) if status.get("models") else "Henüz yüklü model yok"
            if status.get("running"):
                msg = f"✅ Ollama Yerel Servisi Aktif!\nKonum: {status.get('path', 'Bulundu')}\nYüklü Modeller ({len(status.get('models', []))}): {models_txt}\n\n100% Offline ve Ücretsiz olarak kullanıma hazır."
                messagebox.showinfo("Ollama Durumu", msg)
                return
            else:
                messagebox.showerror("Ollama Durumu", "❌ Ollama servisi başlatılamadı. Lütfen 'AI Sunucu Mühendisi' sekmesindeki Yerel AI Hub'dan 'Ollama İndir & Kur' butonunu kullanınız.")
                return

        messagebox.showinfo("Bağlantı Testi", f"[*] {provider_name} servisine ping atılıyor...")

        def _worker():
            resp = self.ai.ask("Ping! Bu bir bağlantı testidir, tek kelime 'OK' yanıtı ver.", provider_name=provider_name, api_key=key)
            if "Hatası" in resp or "Hata" in resp:
                self.parent.after(0, messagebox.showerror, "Test Başarısız", f"{provider_name} Yanıtı:\n{resp}")
            else:
                self.parent.after(0, messagebox.showinfo, "Test Başarılı!", f"✅ {provider_name} başarıyla yanıt verdi:\n\n{resp}")

        threading.Thread(target=_worker, daemon=True).start()


    def save_settings(self):
        cfg = self.config_manager.config

        # Update AI Keys
        for pname, var in self.key_entries.items():
            if pname in cfg["ai"]["providers"]:
                cfg["ai"]["providers"][pname]["api_key"] = var.get().strip()

        # Update Server Settings
        try:
            cfg["server"]["rcon_host"] = self.rcon_host_var.get().strip()
            cfg["server"]["rcon_port"] = int(self.rcon_port_var.get().strip())
            cfg["server"]["rcon_password"] = self.rcon_pass_var.get().strip()
            cfg["server"]["server_port"] = int(self.srv_port_var.get().strip())
            cfg["server"]["bedrock_port"] = int(self.bedrock_port_var.get().strip())
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz port numarası: {e}")
            return

        success = self.config_manager.save(cfg)
        if success:
            messagebox.showinfo("Başarılı", "✅ Tüm ayarlar başarıyla yerel kasaya (config.json) kaydedildi.")
        else:
            messagebox.showerror("Hata", "Ayarlar kaydedilirken bir hata oluştu.")
