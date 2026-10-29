# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: AI Server Engineer & Autonomous Local AI Hub
Unified 12+ AI engines, live model puller with progress bar, and instant crash diagnostics.
"""

import os
import glob
import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.ai_engineer import AIEngineer
from core.local_ai_manager import LocalAIManager, POPULAR_LOCAL_MODELS

class CTkTabAIEngineer(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        self.ai = AIEngineer(config_manager)
        self.local_ai = LocalAIManager(log_callback=self._on_local_ai_log)

        self._build_ui()
        self._refresh_local_status_async()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. ÜST BAR: Sağlayıcı, Model ve Teşhis Butonları
        top_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        top_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))

        top_inner = ctk.CTkFrame(top_card, fg_color="transparent")
        top_inner.pack(fill="x", padx=14, pady=10)

        ctk.CTkLabel(top_inner, text="🤖 AI Sağlayıcı:", font=FONT_BOLD, text_color=COLOR_ACCENT_GOLD).pack(side="left", padx=(0, 6))

        ai_cfg = self.config_manager.get_ai_config()
        providers = list(ai_cfg.get("providers", {}).keys())

        self.prov_var = ctk.StringVar(value=ai_cfg.get("active_provider", "Ollama (Yerel/Ücretsiz)"))
        self.prov_menu = ctk.CTkOptionMenu(
            top_inner,
            variable=self.prov_var,
            values=providers,
            width=200,
            fg_color=COLOR_BG_CARD_HOVER,
            button_color=COLOR_ACCENT_GOLD,
            command=self._on_provider_change
        )
        self.prov_menu.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(top_inner, text="🧠 Model:", font=FONT_BOLD, text_color=COLOR_ACCENT_CYAN).pack(side="left", padx=(0, 6))
        self.model_var = ctk.StringVar(value=ai_cfg.get("active_model", "qwen2.5:1.5b"))
        self.model_entry = ctk.CTkEntry(top_inner, textvariable=self.model_var, width=150, font=FONT_CODE, fg_color="#030712")
        self.model_entry.pack(side="left", padx=(0, 12))

        # Teşhis Butonları
        btn_diag = ctk.CTkButton(
            top_inner,
            text="🚨 Çökmeyi Teşhis Et",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_RED,
            hover_color="#dc2626",
            height=32,
            command=self.diagnose_last_crash
        )
        btn_diag.pack(side="right", padx=(6, 0))

        btn_opt = ctk.CTkButton(
            top_inner,
            text="⚡ Lag Optimizasyonu",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_PURPLE,
            hover_color="#7c3aed",
            height=32,
            command=self.optimize_config
        )
        btn_opt.pack(side="right", padx=(6, 0))

        # 2. ORTA BAR: Otonom Yerel AI İstasyonu (Local AI Hub)
        self.local_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        self.local_card.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))

        loc_top = ctk.CTkFrame(self.local_card, fg_color="transparent")
        loc_top.pack(fill="x", padx=14, pady=(10, 6))

        ctk.CTkLabel(loc_top, text="🛡️ YEREL AI MERKEZİ (%100 Çevrimdışı, Güvenli, Sınırsız & Ücretsiz)", font=FONT_BOLD, text_color=COLOR_ACCENT_GREEN).pack(side="left")

        self.lbl_ollama_stat = ctk.CTkLabel(loc_top, text="● Ollama: Kontrol ediliyor...", font=FONT_SMALL, text_color=COLOR_ACCENT_GOLD)
        self.lbl_ollama_stat.pack(side="left", padx=14)

        self.btn_install_ollama = ctk.CTkButton(
            loc_top,
            text="📥 1-Tıkla Ollama İndir & Kur",
            font=FONT_SMALL,
            width=160,
            height=26,
            fg_color=COLOR_ACCENT_CYAN,
            text_color="#000000",
            command=self._start_install_ollama
        )
        self.btn_install_ollama.pack(side="left", padx=6)

        self.btn_start_service = ctk.CTkButton(
            loc_top,
            text="▶️ Servisi Başlat",
            font=FONT_SMALL,
            width=110,
            height=26,
            fg_color=COLOR_BG_CARD_HOVER,
            command=self._start_ollama_service
        )
        self.btn_start_service.pack(side="left", padx=6)

        btn_ref = ctk.CTkButton(
            loc_top,
            text="🔄 Yenile",
            font=FONT_SMALL,
            width=60,
            height=26,
            fg_color=COLOR_BG_CARD_HOVER,
            command=self._refresh_local_status_async
        )
        btn_ref.pack(side="right")

        # Model İndirme Satırı
        dl_row = ctk.CTkFrame(self.local_card, fg_color="transparent")
        dl_row.pack(fill="x", padx=14, pady=(0, 8))

        ctk.CTkLabel(dl_row, text="📦 Model İndir:", font=FONT_SMALL, text_color=COLOR_TEXT_MAIN).pack(side="left", padx=(0, 6))

        preset_names = [f"{m[0]} - {m[1]}" for m in POPULAR_LOCAL_MODELS]
        self.pull_var = ctk.StringVar(value=preset_names[0] if preset_names else "")
        self.pull_menu = ctk.CTkOptionMenu(dl_row, variable=self.pull_var, values=preset_names, width=320, fg_color=COLOR_BG_CARD_HOVER)
        self.pull_menu.pack(side="left", padx=(0, 8))

        self.btn_pull = ctk.CTkButton(
            dl_row,
            text="⚡ Modeli İndir",
            font=FONT_SMALL,
            width=110,
            height=28,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            command=self._start_pull_model
        )
        self.btn_pull.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(dl_row, text="Yüklü Modeller:", font=FONT_SMALL, text_color=COLOR_ACCENT_GOLD).pack(side="left", padx=(0, 6))
        self.installed_var = ctk.StringVar(value="Yok")
        self.installed_menu = ctk.CTkOptionMenu(dl_row, variable=self.installed_var, values=["Yok"], width=130, fg_color=COLOR_BG_CARD_HOVER, command=self._on_installed_selected)
        self.installed_menu.pack(side="left")

        # Progress bar
        prog_row = ctk.CTkFrame(self.local_card, fg_color="transparent")
        prog_row.pack(fill="x", padx=14, pady=(0, 8))

        self.prog_bar = ctk.CTkProgressBar(prog_row, height=8, progress_color=COLOR_ACCENT_CYAN)
        self.prog_bar.set(0)
        self.prog_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.lbl_prog_text = ctk.CTkLabel(prog_row, text="Hazır", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        self.lbl_prog_text.pack(side="right")

        # 3. ALT ALAN: AI Sohbet ve Çıktı Ekranı
        chat_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        chat_card.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        chat_card.grid_columnconfigure(0, weight=1)
        chat_card.grid_rowconfigure(1, weight=1)

        chat_head = ctk.CTkFrame(chat_card, fg_color="transparent")
        chat_head.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 4))
        ctk.CTkLabel(chat_head, text="💬 AI SUNUCU MÜHENDİSİ DANIŞMA PANELİ", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_GREEN).pack(side="left")

        btn_cls = ctk.CTkButton(chat_head, text="Temizle", font=FONT_SMALL, width=64, height=24, fg_color=COLOR_BG_CARD_HOVER, command=lambda: self.chat_box.delete("1.0", "end"))
        btn_cls.pack(side="right")

        self.chat_box = ctk.CTkTextbox(chat_card, fg_color="#030712", text_color="#f8fafc", font=FONT_REGULAR, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        self.chat_box.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))

        # Mesaj Giriş Barı
        input_bar = ctk.CTkFrame(chat_card, fg_color="transparent")
        input_bar.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 12))

        self.input_entry = ctk.CTkEntry(input_bar, placeholder_text="AI Mühendisine bir soru sor (örn: 'Arclight 1.20.1 sunucumda TPS neden düşüyor?')", font=FONT_REGULAR, fg_color="#030712", height=38)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        btn_send = ctk.CTkButton(input_bar, text="Gönder", font=FONT_BOLD, fg_color=COLOR_ACCENT_CYAN, text_color="#000000", width=90, height=38, command=self.send_message)
        btn_send.pack(side="right")

        self.append_chat("🤖 Merhaba! Ben AI Minecraft Sunucu Mühendisi. 12 farklı bulut motoru veya %100 çevrimdışı yerel AI ile sunucunu kurmana, hataları çözmene ve lag optimizasyonu yapmana hazırım.\n")

    def append_chat(self, text):
        self.chat_box.insert("end", f"{text}\n")
        self.chat_box.see("end")

    def _on_local_ai_log(self, msg):
        self.after(0, lambda: self.lbl_prog_text.configure(text=msg))

    def _refresh_local_status_async(self):
        def _worker():
            try:
                st = self.local_ai.get_status()
                self.after(0, self._apply_local_status, st)
            except Exception:
                pass
        threading.Thread(target=_worker, daemon=True).start()

    def _apply_local_status(self, st):
        installed = st.get("installed", False)
        running = st.get("running", False)
        models = st.get("models", [])

        if installed and running:
            self.lbl_ollama_stat.configure(text="● Ollama: Aktif 🟢", text_color=COLOR_ACCENT_GREEN)
            self.btn_install_ollama.configure(state="disabled", text="✅ Kurulu")
            self.btn_start_service.configure(state="disabled", text="✅ Çalışıyor")
        elif installed:
            self.lbl_ollama_stat.configure(text="● Servis: Kapalı 🟡", text_color=COLOR_ACCENT_GOLD)
            self.btn_install_ollama.configure(state="disabled", text="✅ Kurulu")
            self.btn_start_service.configure(state="normal", text="▶️ Başlat")
        else:
            self.lbl_ollama_stat.configure(text="● Ollama: Yok 🔴", text_color=COLOR_ACCENT_RED)
            self.btn_install_ollama.configure(state="normal", text="📥 İndir & Kur")
            self.btn_start_service.configure(state="disabled", text="▶️ Başlat")

        if models:
            self.installed_menu.configure(values=models)
            if self.installed_var.get() not in models:
                self.installed_var.set(models[0])
                if "Ollama" in self.prov_var.get():
                    self.model_var.set(models[0])

    def _start_install_ollama(self):
        self.btn_install_ollama.configure(state="disabled", text="⏳ İndiriliyor...")
        def _worker():
            ok = self.local_ai.download_and_install_ollama(status_callback=lambda msg: self.after(0, lambda: self.lbl_prog_text.configure(text=msg)))
            self._refresh_local_status_async()
            if ok:
                self.after(0, messagebox.showinfo, "Ollama", "✅ Kurulum başlatıldı! Tamamlandıktan sonra 'Servisi Başlat' butonuna basabilirsiniz.")
        threading.Thread(target=_worker, daemon=True).start()

    def _start_ollama_service(self):
        def _worker():
            ok = self.local_ai.ensure_service_running()
            self._refresh_local_status_async()
            if ok:
                self.after(0, lambda: self.lbl_prog_text.configure(text="✅ Ollama servisi aktif edildi!"))
        threading.Thread(target=_worker, daemon=True).start()

    def _start_pull_model(self):
        sel = self.pull_var.get()
        if not sel:
            return
        m_name = sel.split(" - ")[0].strip()
        self.btn_pull.configure(state="disabled", text="⏳ İndiriliyor...")
        self.prog_bar.set(0)

        def _prog(pct, msg):
            self.after(0, lambda: self.prog_bar.set(pct / 100.0))
            self.after(0, lambda: self.lbl_prog_text.configure(text=msg))

        def _worker():
            ok = self.local_ai.pull_model_stream(m_name, progress_callback=_prog)
            self.after(0, lambda: self.btn_pull.configure(state="normal", text="⚡ Modeli İndir"))
            self._refresh_local_status_async()
            if ok:
                self.after(0, lambda: self.model_var.set(m_name))
                self.after(0, messagebox.showinfo, "Model Hazır", f"🎉 '{m_name}' modeli başarıyla indirildi ve aktif edildi!")

        threading.Thread(target=_worker, daemon=True).start()

    def _on_installed_selected(self, val):
        if "Ollama" in self.prov_var.get():
            self.model_var.set(val)

    def _on_provider_change(self, val):
        ai_cfg = self.config_manager.get_ai_config()
        providers = ai_cfg.get("providers", {})
        if val in providers:
            def_m = providers[val].get("default_model", "")
            if "Ollama" in val:
                models = self.local_ai.list_local_models()
                if models:
                    def_m = models[0]
            self.model_var.set(def_m)
            ai_cfg["active_provider"] = val
            ai_cfg["active_model"] = def_m
            self.config_manager.save()

    def send_message(self):
        msg = self.input_entry.get().strip()
        if not msg:
            return
        self.input_entry.delete(0, "end")
        self.append_chat(f"\n👤 Siz: {msg}")
        self.append_chat("🤖 Düşünüyor...")

        prov = self.prov_var.get()
        model = self.model_var.get()

        def _worker():
            resp = self.ai.ask(msg, provider_name=prov, model=model)
            def _render():
                box_txt = self.chat_box.get("1.0", "end")
                if "🤖 Düşünüyor..." in box_txt:
                    idx = box_txt.rfind("🤖 Düşünüyor...")
                    self.chat_box.delete(f"1.0 + {idx} chars", f"1.0 + {idx + len('🤖 Düşünüyor...')} chars")
                self.append_chat(f"🤖 AI Mühendis:\n{resp}\n")
            self.after(0, _render)

        threading.Thread(target=_worker, daemon=True).start()

    def diagnose_last_crash(self):
        cfg = self.config_manager.get_server_config()
        sdir = cfg.get("server_dir", os.path.join(os.getcwd(), "server"))
        crash_dir = os.path.join(sdir, "crash-reports")
        log_file = os.path.join(sdir, "logs", "latest.log")

        snippet, src = "", ""
        if os.path.exists(crash_dir):
            crashes = glob.glob(os.path.join(crash_dir, "*.txt"))
            if crashes:
                crashes.sort(key=os.path.getmtime, reverse=True)
                latest = crashes[0]
                src = os.path.basename(latest)
                with open(latest, "r", encoding="utf-8", errors="replace") as f:
                    snippet = f.read()[-3500:]

        if not snippet and os.path.exists(log_file):
            src = "latest.log"
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                snippet = "".join(f.readlines()[-150:])

        if not snippet:
            messagebox.showinfo("Bilgi", "İncelenecek bir çökme raporu veya hata logu bulunamadı.")
            return

        self.append_chat(f"\n🚨 [Sistem] {src} incelenmek üzere AI Mühendisine iletiliyor...")
        prov = self.prov_var.get()

        def _worker():
            resp = self.ai.analyze_log_error(snippet, provider_name=prov)
            self.after(0, lambda: self.append_chat(f"🤖 AI Teşhis Sonucu:\n{resp}\n"))
        threading.Thread(target=_worker, daemon=True).start()

    def optimize_config(self):
        cfg = self.config_manager.get_server_config()
        ver = cfg.get("mc_version", "1.20.1")
        stype = cfg.get("server_type", "Paper")
        ram = cfg.get("max_ram_gb", 6)

        self.append_chat(f"\n⚡ [Sistem] {ver} ({stype}, {ram}GB RAM) için optimizasyon kuralları oluşturuluyor...")
        def _worker():
            resp = self.ai.optimize_server(player_count=20, ram_gb=ram, server_type=stype, mc_version=ver)
            self.after(0, lambda: self.append_chat(f"🤖 AI Optimizasyon Önerileri:\n{resp}\n"))
        threading.Thread(target=_worker, daemon=True).start()
