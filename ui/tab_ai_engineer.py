# -*- coding: utf-8 -*-
"""
Tab: AI Server Engineer & Crash Diagnostics (12+ Providers & Autonomous Local AI Hub)
"""

import os
import glob
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from ui.theme import *
from core.ai_engineer import AIEngineer
from core.local_ai_manager import LocalAIManager, POPULAR_LOCAL_MODELS

class TabAIEngineer:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        self.ai = AIEngineer(config_manager)
        self.local_ai = LocalAIManager(log_callback=self._on_local_ai_log)
        self.frame = tk.Frame(parent, bg=BG_DARK)

        self._build_ui()
        self._refresh_local_status_async()

    def _build_ui(self):
        # 1. ÜST BAR: Sağlayıcı ve Model Seçimi + Teşhis Butonları
        top_bar = tk.Frame(self.frame, bg=BG_PANEL, padx=14, pady=8)
        top_bar.pack(fill=tk.X, side=tk.TOP, pady=(0, 4))

        lbl_prov = tk.Label(top_bar, text="🤖 AI Motoru:", font=("Segoe UI", 9, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL)
        lbl_prov.pack(side=tk.LEFT, padx=(0, 6))

        ai_cfg = self.config_manager.get_ai_config()
        providers = list(ai_cfg.get("providers", {}).keys())

        self.prov_var = tk.StringVar(value=ai_cfg.get("active_provider", "Ollama (Yerel/Ücretsiz)"))
        self.prov_combo = ttk.Combobox(
            top_bar,
            textvariable=self.prov_var,
            font=("Segoe UI", 9, "bold"),
            values=providers,
            width=22,
            state="readonly"
        )
        self.prov_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.prov_combo.bind("<<ComboboxSelected>>", self._on_provider_change)

        lbl_mod = tk.Label(top_bar, text="🧠 Model:", font=("Segoe UI", 9, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL)
        lbl_mod.pack(side=tk.LEFT, padx=(0, 6))

        self.model_var = tk.StringVar(value=ai_cfg.get("active_model", "qwen2.5:1.5b"))
        self.model_entry = tk.Entry(
            top_bar,
            textvariable=self.model_var,
            font=("Consolas", 9),
            bg=BG_CARD,
            fg="#ffffff",
            relief=tk.FLAT,
            width=22
        )
        self.model_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=2)

        # Yerel AI Paneli Aç/Kapat Butonu
        self.btn_toggle_local = tk.Button(
            top_bar,
            text="⚡ Yerel AI Hub (Offline)",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            command=self._toggle_local_panel
        )
        self.btn_toggle_local.pack(side=tk.LEFT, padx=4)

        # Hızlı Teşhis & Optimizasyon Butonları
        btn_diag = tk.Button(
            top_bar,
            text="🚨 Çökmeyi Teşhis Et",
            font=("Segoe UI", 8, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            relief=tk.FLAT,
            padx=10,
            command=self.diagnose_last_crash
        )
        btn_diag.pack(side=tk.RIGHT, padx=3)

        btn_opt = tk.Button(
            top_bar,
            text="⚡ Lag Optimizasyonu",
            font=("Segoe UI", 8, "bold"),
            bg="#7c3aed",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            command=self.optimize_config
        )
        btn_opt.pack(side=tk.RIGHT, padx=3)

        # 2. YEREL AI YÖNETİM VE İNDİRME PANELİ (OFFLINE / 1-CLICK)
        self.local_panel = tk.LabelFrame(
            self.frame,
            text=" 🛡️ YEREL AI MERKEZİ (100% Çevrimdışı, Güvenli, Sınırsız & Ücretsiz) ",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_GREEN,
            bg=BG_PANEL,
            padx=12,
            pady=8
        )
        self.local_panel.pack(fill=tk.X, padx=8, pady=(0, 4))

        # Durum Satırı
        stat_frame = tk.Frame(self.local_panel, bg=BG_PANEL)
        stat_frame.pack(fill=tk.X, pady=(0, 6))

        self.lbl_ollama_install = tk.Label(stat_frame, text="● Ollama: Kontrol ediliyor...", font=("Segoe UI", 8, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL)
        self.lbl_ollama_install.pack(side=tk.LEFT, padx=(0, 14))

        self.lbl_ollama_service = tk.Label(stat_frame, text="● Servis: Bekleniyor...", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_PANEL)
        self.lbl_ollama_service.pack(side=tk.LEFT, padx=(0, 14))

        self.btn_install_ollama = tk.Button(
            stat_frame,
            text="📥 1-Tıkla Ollama İndir & Kur",
            font=("Segoe UI", 8, "bold"),
            bg=ACCENT_CYAN,
            fg="#000000",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            command=self._start_install_ollama
        )
        self.btn_install_ollama.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_start_service = tk.Button(
            stat_frame,
            text="▶️ Servisi Başlat (ollama serve)",
            font=("Segoe UI", 8),
            bg=BG_CARD,
            fg=ACCENT_GREEN,
            relief=tk.FLAT,
            padx=8,
            pady=2,
            command=self._start_ollama_service
        )
        self.btn_start_service.pack(side=tk.LEFT, padx=(0, 8))

        btn_refresh = tk.Button(
            stat_frame,
            text="🔄 Yenile",
            font=("Segoe UI", 8),
            bg=BG_CARD,
            fg=TEXT_COLOR,
            relief=tk.FLAT,
            padx=6,
            pady=2,
            command=self._refresh_local_status_async
        )
        btn_refresh.pack(side=tk.RIGHT)

        # Model İndirme Satırı
        dl_frame = tk.Frame(self.local_panel, bg=BG_PANEL)
        dl_frame.pack(fill=tk.X, pady=(2, 4))

        tk.Label(dl_frame, text="📦 Popüler Model İndir:", font=("Segoe UI", 8, "bold"), fg=TEXT_COLOR, bg=BG_PANEL).pack(side=tk.LEFT, padx=(0, 6))

        preset_names = [f"{m[0]} - {m[1]}" for m in POPULAR_LOCAL_MODELS]
        self.pull_combo_var = tk.StringVar(value=preset_names[0] if preset_names else "")
        self.pull_combo = ttk.Combobox(dl_frame, textvariable=self.pull_combo_var, values=preset_names, width=54, state="readonly")
        self.pull_combo.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_pull_model = tk.Button(
            dl_frame,
            text="⚡ Modeli İndir & Kur",
            font=("Segoe UI", 8, "bold"),
            bg=ACCENT_GREEN,
            fg="#000000",
            relief=tk.FLAT,
            padx=10,
            command=self._start_pull_model
        )
        self.btn_pull_model.pack(side=tk.LEFT)

        # Yüklü Modeller
        tk.Label(dl_frame, text="Yüklü Modellerim:", font=("Segoe UI", 8, "bold"), fg=ACCENT_GOLD, bg=BG_PANEL).pack(side=tk.LEFT, padx=(14, 6))
        self.installed_models_var = tk.StringVar()
        self.installed_combo = ttk.Combobox(dl_frame, textvariable=self.installed_models_var, width=18, state="readonly")
        self.installed_combo.pack(side=tk.LEFT, padx=(0, 6))
        self.installed_combo.bind("<<ComboboxSelected>>", self._on_installed_model_selected)

        # Progress Bar & Progress Label
        self.prog_frame = tk.Frame(self.local_panel, bg=BG_PANEL)
        self.prog_frame.pack(fill=tk.X, pady=(2, 0))

        self.progress_bar = ttk.Progressbar(self.prog_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.lbl_progress = tk.Label(self.prog_frame, text="Hazır", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w")
        self.lbl_progress.pack(side=tk.RIGHT, fill=tk.X)

        # 3. ORTA ALAN: AI Sohbet Ekranı
        chat_frame = tk.Frame(self.frame, bg=BG_PANEL, padx=14, pady=8)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=2)

        head = tk.Frame(chat_frame, bg=BG_PANEL)
        head.pack(fill=tk.X, pady=(0, 4))
        tk.Label(head, text="💬 AI SUNUCU MÜHENDİSİ DANIŞMA PANELİ", font=("Segoe UI", 9, "bold"), fg=ACCENT_GREEN, bg=BG_PANEL).pack(side=tk.LEFT)

        btn_clear = tk.Button(head, text="Sohbeti Temizle", font=("Segoe UI", 7), bg=BG_CARD, fg=TEXT_MUTED, relief=tk.FLAT, padx=6, command=lambda: self.chat_area.delete("1.0", tk.END))
        btn_clear.pack(side=tk.RIGHT)

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            bg="#030712",
            fg="#e2e8f0",
            insertbackground=ACCENT_CYAN,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.chat_area.tag_config("user", foreground=ACCENT_CYAN, font=("Segoe UI", 10, "bold"))
        self.chat_area.tag_config("ai", foreground="#f8fafc", font=("Segoe UI", 10))
        self.chat_area.tag_config("system", foreground=ACCENT_GOLD, font=("Segoe UI", 9, "italic"))

        self.append_chat("🤖 Merhaba! Ben AI Minecraft Sunucu Mühendisi. 12 farklı sağlayıcı veya %100 çevrimdışı Yerel AI ile sunucunu kurmana, arızaları çözmene ve lag optimizasyonu yapmana yardımcı olmaya hazırım.\n", "ai")

        # 4. ALT BAR: Mesaj Girişi
        input_bar = tk.Frame(self.frame, bg=BG_PANEL, padx=14, pady=8)
        input_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=(0, 8))

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_bar,
            textvariable=self.input_var,
            font=("Segoe UI", 10),
            bg=BG_CARD,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=4)
        self.input_entry.bind("<Return>", lambda e: self.send_user_message())

        btn_send = tk.Button(
            input_bar,
            text="Gönder (Enter)",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_CYAN,
            fg="#000000",
            activebackground="#0284c7",
            relief=tk.FLAT,
            padx=16,
            command=self.send_user_message
        )
        btn_send.pack(side=tk.RIGHT)

    def _toggle_local_panel(self):
        if self.local_panel.winfo_ismapped():
            self.local_panel.pack_forget()
            self.btn_toggle_local.configure(text="⚡ Yerel AI Hub (Aç)")
        else:
            self.local_panel.pack(fill=tk.X, padx=8, pady=(0, 4), after=self.frame.winfo_children()[0])
            self.btn_toggle_local.configure(text="⚡ Yerel AI Hub (Kapat)")

    def _on_local_ai_log(self, msg):
        self.parent.after(0, lambda: self.lbl_progress.configure(text=msg))

    def _refresh_local_status_async(self):
        def _worker():
            status = self.local_ai.get_status()
            self.parent.after(0, self._apply_local_status, status)
        threading.Thread(target=_worker, daemon=True).start()

    def _apply_local_status(self, status):
        installed = status.get("installed", False)
        running = status.get("running", False)
        models = status.get("models", [])

        if installed:
            self.lbl_ollama_install.configure(text="● Ollama: Yüklü 🟢", fg=ACCENT_GREEN)
            self.btn_install_ollama.configure(state="disabled", text="✅ Ollama Kurulu")
        else:
            self.lbl_ollama_install.configure(text="● Ollama: Kurulu Değil 🔴", fg=ACCENT_RED)
            self.btn_install_ollama.configure(state="normal", text="📥 1-Tıkla Ollama İndir & Kur")

        if running:
            self.lbl_ollama_service.configure(text="● Servis: Aktif (11434) 🟢", fg=ACCENT_GREEN)
            self.btn_start_service.configure(state="disabled", text="✅ Servis Çalışıyor")
        else:
            self.lbl_ollama_service.configure(text="● Servis: Kapalı 🟡", fg=ACCENT_GOLD)
            self.btn_start_service.configure(state="normal", text="▶️ Servisi Başlat")

        # Modelleri güncelle
        self.installed_combo["values"] = models
        if models:
            if not self.installed_models_var.get() or self.installed_models_var.get() not in models:
                self.installed_models_var.set(models[0])
                if "Ollama" in self.prov_var.get():
                    self.model_var.set(models[0])

    def _start_install_ollama(self):
        self.btn_install_ollama.configure(state="disabled", text="⏳ İndiriliyor...")
        def _worker():
            success = self.local_ai.download_and_install_ollama(
                status_callback=lambda msg: self.parent.after(0, lambda: self.lbl_progress.configure(text=msg))
            )
            self._refresh_local_status_async()
            if success:
                self.parent.after(0, messagebox.showinfo, "Ollama Kurulumu", "✅ Ollama kurulumu başlatıldı. Kurulum tamamlandıktan sonra 'Servisi Başlat' butonuna tıklayabilirsiniz.")
        threading.Thread(target=_worker, daemon=True).start()

    def _start_ollama_service(self):
        def _worker():
            self.parent.after(0, lambda: self.lbl_progress.configure(text="Ollama servisi başlatılıyor..."))
            ok = self.local_ai.ensure_service_running()
            self._refresh_local_status_async()
            if ok:
                self.parent.after(0, lambda: self.lbl_progress.configure(text="✅ Ollama servisi başarıyla aktif!"))
            else:
                self.parent.after(0, lambda: self.lbl_progress.configure(text="❌ Servis başlatılamadı. Ollama kurulu mu?"))
        threading.Thread(target=_worker, daemon=True).start()

    def _start_pull_model(self):
        sel = self.pull_combo_var.get()
        if not sel:
            return
        model_name = sel.split(" - ")[0].strip()

        self.btn_pull_model.configure(state="disabled", text="⏳ İndiriliyor...")
        self.progress_bar["value"] = 0

        def _progress(pct, msg):
            def _ui():
                self.progress_bar["value"] = pct
                self.lbl_progress.configure(text=msg)
            self.parent.after(0, _ui)

        def _worker():
            success = self.local_ai.pull_model_stream(model_name, progress_callback=_progress)
            self.parent.after(0, lambda: self.btn_pull_model.configure(state="normal", text="⚡ Modeli İndir & Kur"))
            self._refresh_local_status_async()
            if success:
                self.parent.after(0, lambda: self.model_var.set(model_name))
                self.parent.after(0, messagebox.showinfo, "Model Hazır!", f"🎉 '{model_name}' modeli başarıyla indirildi ve kullanıma hazır!")

        threading.Thread(target=_worker, daemon=True).start()

    def _on_installed_model_selected(self, event=None):
        mod = self.installed_models_var.get()
        if mod and "Ollama" in self.prov_var.get():
            self.model_var.set(mod)
            ai_cfg = self.config_manager.get_ai_config()
            ai_cfg["active_model"] = mod
            self.config_manager.save()

    def _on_provider_change(self, event=None):
        prov = self.prov_var.get()
        ai_cfg = self.config_manager.get_ai_config()
        providers_dict = ai_cfg.get("providers", {})
        if prov in providers_dict:
            def_model = providers_dict[prov].get("default_model", "")
            if "Ollama" in prov:
                models = self.local_ai.list_local_models()
                if models:
                    def_model = models[0]
            self.model_var.set(def_model)
            ai_cfg["active_provider"] = prov
            ai_cfg["active_model"] = def_model
            self.config_manager.save()

    def append_chat(self, text, tag="ai"):
        self.chat_area.insert(tk.END, text + "\n", tag)
        self.chat_area.see(tk.END)

    def send_user_message(self):
        msg = self.input_var.get().strip()
        if not msg:
            return
        self.input_var.set("")
        self.append_chat(f"\n👤 Siz: {msg}", "user")
        self.append_chat("🤖 Düşünüyor...", "system")

        prov = self.prov_var.get()
        model = self.model_var.get()

        def _worker():
            resp = self.ai.ask(msg, provider_name=prov, model=model)
            self.parent.after(0, self._render_response, resp)

        threading.Thread(target=_worker, daemon=True).start()

    def _render_response(self, response_text):
        content = self.chat_area.get("1.0", tk.END)
        if "🤖 Düşünüyor..." in content:
            idx = content.rfind("🤖 Düşünüyor...")
            self.chat_area.delete(f"1.0 + {idx} chars", f"1.0 + {idx + len('🤖 Düşünüyor...')} chars")
        self.append_chat(f"🤖 AI Mühendis:\n{response_text}\n", "ai")

    def diagnose_last_crash(self):
        cfg = self.config_manager.get_server_config()
        sdir = cfg.get("server_dir", os.path.join(os.getcwd(), "server"))

        crash_dir = os.path.join(sdir, "crash-reports")
        log_file = os.path.join(sdir, "logs", "latest.log")

        snippet = ""
        src_name = ""

        if os.path.exists(crash_dir):
            crashes = glob.glob(os.path.join(crash_dir, "*.txt"))
            if crashes:
                crashes.sort(key=os.path.getmtime, reverse=True)
                latest_crash = crashes[0]
                src_name = os.path.basename(latest_crash)
                with open(latest_crash, "r", encoding="utf-8", errors="replace") as f:
                    snippet = f.read()[-3500:]

        if not snippet and os.path.exists(log_file):
            src_name = "latest.log"
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                snippet = "".join(lines[-150:])

        if not snippet:
            messagebox.showinfo("Bilgi", "İncelenecek bir çökme raporu veya hata logu bulunamadı.")
            return

        self.append_chat(f"\n🚨 [Sistem] {src_name} dosyası incelenmek üzere AI Sağlayıcısına iletiliyor...", "system")
        prov = self.prov_var.get()

        def _worker():
            resp = self.ai.analyze_log_error(snippet, provider_name=prov)
            self.parent.after(0, self._render_response, resp)

        threading.Thread(target=_worker, daemon=True).start()

    def optimize_config(self):
        cfg = self.config_manager.get_server_config()
        ver = cfg.get("mc_version", "1.20.1")
        stype = cfg.get("server_type", "Paper")
        ram = cfg.get("max_ram_gb", 6)

        self.append_chat(f"\n⚡ [Sistem] {ver} ({stype}, {ram}GB RAM) için optimizasyon kuralları oluşturuluyor...", "system")
        prov = self.prov_var.get()

        def _worker():
            resp = self.ai.optimize_server(player_count=20, ram_gb=ram, server_type=stype, mc_version=ver)
            self.parent.after(0, self._render_response, resp)

        threading.Thread(target=_worker, daemon=True).start()

