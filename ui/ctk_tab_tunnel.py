# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: Global Multi-Tunnel & Multiplayer Port Forwarding Hub
Matches All User Requirements:
- Playit.gg (Zero-config free global Minecraft domain *.gl.at.ply.gg:port)
- Cloudflare Tunnel (cloudflared zero-trust TCP tunnel)
- ngrok TCP (ngrok tcp 25565 with custom authtoken support)
- Localtonet (TCP tunnel client)
- Modem UPnP (Automated SSDP router port forward test)
- 1-Click Copy Public Address Banner
- Live Terminal Logging
"""

import re
import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.tunnel_manager import TunnelManager

class CTkTabTunnel(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        self.tunnel = TunnelManager(log_callback=self._on_log, address_callback=self._on_address_found)
        self.extracted_address = None

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # 1. Video Banner: "ARKADAŞLARIN ANINDA GİRSİN"
        hero_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_ACCENT_CYAN)
        hero_card.pack(fill="x", padx=0, pady=(0, 10))

        h_inner = ctk.CTkFrame(hero_card, fg_color="transparent")
        h_inner.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(h_inner, text="🌐 ARKADAŞLARIN DÜNYANIN HER YERİNDEN GİRSİN", font=FONT_TITLE, text_color=COLOR_ACCENT_CYAN).pack(anchor="w")
        ctk.CTkLabel(
            h_inner,
            text="Playit.gg • Cloudflare Tunnel • ngrok TCP • Localtonet • Modem UPnP | Port açma yok, modem şifresi yok.",
            font=FONT_REGULAR,
            text_color=COLOR_TEXT_MAIN
        ).pack(anchor="w", pady=(2, 0))

        # 2. Hızlı Bağlantı Adresi ve Kopyalama Kutusu
        addr_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD_HOVER, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        addr_card.pack(fill="x", padx=0, pady=(0, 10))

        addr_row = ctk.CTkFrame(addr_card, fg_color="transparent")
        addr_row.pack(fill="x", padx=14, pady=10)

        ctk.CTkLabel(addr_row, text="🔗 Aktif Sunucu Adresi:", font=FONT_BOLD, text_color=COLOR_ACCENT_GOLD).pack(side="left", padx=(0, 10))

        self.lbl_address = ctk.CTkEntry(
            addr_row,
            font=FONT_CODE,
            height=32,
            fg_color="#030712",
            text_color=COLOR_ACCENT_GREEN,
            border_color=COLOR_BORDER
        )
        self.lbl_address.insert(0, "Tünel başlatıldığında adres burada belirecektir (örn: ornek.gl.at.ply.gg:12345 veya 0.tcp.ngrok.io:12345)")
        self.lbl_address.configure(state="readonly")
        self.lbl_address.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_copy = ctk.CTkButton(
            addr_row,
            text="📋 Adresi Kopyala",
            font=FONT_BOLD,
            width=130,
            height=32,
            fg_color=COLOR_ACCENT_CYAN,
            text_color="#000000",
            hover_color="#38bdf8",
            command=self._copy_address
        )
        self.btn_copy.pack(side="right")

        # 3. Sağlayıcı Seçici & Kontrol Kartı
        ctrl_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        ctrl_card.pack(fill="x", padx=0, pady=(0, 10))

        ctrl_inner = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        ctrl_inner.pack(fill="x", padx=16, pady=10)

        # Provider Button Row 1: Tüneller
        row1 = ctk.CTkFrame(ctrl_inner, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))

        self.btn_playit = ctk.CTkButton(
            row1,
            text="⚡ Playit.gg Başlat",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            hover_color="#34d399",
            height=36,
            command=self._start_playit
        )
        self.btn_playit.pack(side="left", padx=(0, 8))

        self.btn_cf = ctk.CTkButton(
            row1,
            text="☁️ Cloudflare Tunnel",
            font=FONT_BOLD,
            fg_color="#f97316",
            text_color="#000000",
            hover_color="#fb923c",
            height=36,
            command=self._start_cloudflare
        )
        self.btn_cf.pack(side="left", padx=(0, 8))

        self.btn_ngrok = ctk.CTkButton(
            row1,
            text="🚀 ngrok TCP Başlat",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_CYAN,
            text_color="#000000",
            hover_color="#38bdf8",
            height=36,
            command=self._start_ngrok
        )
        self.btn_ngrok.pack(side="left", padx=(0, 8))

        self.btn_localtonet = ctk.CTkButton(
            row1,
            text="🌐 Localtonet Başlat",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_PURPLE,
            text_color="#ffffff",
            hover_color="#a855f7",
            height=36,
            command=self._start_localtonet
        )
        self.btn_localtonet.pack(side="left", padx=(0, 8))

        self.btn_upnp = ctk.CTkButton(
            row1,
            text="📡 Modem UPnP Test Et",
            font=FONT_BOLD,
            fg_color=COLOR_BG_CARD_HOVER,
            hover_color=COLOR_BORDER,
            height=36,
            command=self._test_upnp
        )
        self.btn_upnp.pack(side="left", padx=(0, 8))

        self.btn_stop = ctk.CTkButton(
            row1,
            text="⏹️ Tüneli Durdur",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_RED,
            hover_color="#dc2626",
            height=36,
            command=self._stop_tunnel
        )
        self.btn_stop.pack(side="right")

        # Row 2: ngrok / Tünel Ayarları (Authtoken ve Port Girişi)
        row2 = ctk.CTkFrame(ctrl_inner, fg_color="transparent")
        row2.pack(fill="x")

        ctk.CTkLabel(row2, text="🔑 ngrok Authtoken (İsteğe bağlı):", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))
        self.ngrok_token_var = ctk.StringVar()
        cfg = self.config_manager.get_server_config()
        saved_token = cfg.get("ngrok_authtoken", "")
        self.ngrok_token_var.set(saved_token)
        self.ngrok_entry = ctk.CTkEntry(
            row2,
            textvariable=self.ngrok_token_var,
            placeholder_text="ngrok hesabınızdan aldığınız authtoken'ı yapıştırın (opsiyonel)",
            font=FONT_SMALL,
            height=28,
            fg_color="#030712",
            border_color=COLOR_BORDER,
            width=380
        )
        self.ngrok_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkLabel(row2, text="🔌 Port:", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(side="left", padx=(0, 4))
        self.port_var = ctk.StringVar(value=str(cfg.get("server_port", 25565)))
        self.port_entry = ctk.CTkEntry(row2, textvariable=self.port_var, font=FONT_SMALL, width=65, height=28, fg_color="#030712", border_color=COLOR_BORDER)
        self.port_entry.pack(side="left")

        # 4. Canlı Tünel Konsolu
        log_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        log_card.pack(fill="both", expand=True, padx=0, pady=0)

        ctk.CTkLabel(log_card, text="📜 CANLI TÜNEL & BAĞLANTI DURUM LOGLARI", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=16, pady=(10, 6))

        self.tunnel_log = ctk.CTkTextbox(log_card, fg_color="#030712", text_color="#f8fafc", font=FONT_CODE, corner_radius=8)
        self.tunnel_log.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self._on_log("🌐 Çoklu Tünel Yöneticisi v3.8.0 hazır.")
        self._on_log("> Desteklenen altyapılar: Playit.gg, Cloudflare Tunnel, ngrok TCP, Localtonet ve UPnP.")
        self._on_log("> İstediğiniz sağlayıcı butonuna tıklayarak tüneli tek tıkla başlatabilirsiniz.")

    def _on_log(self, msg):
        self.after(0, lambda: self._insert_log(msg))

    def _insert_log(self, msg):
        self.tunnel_log.insert("end", f"{msg}\n")
        self.tunnel_log.see("end")

        # Otomatik bağlantı adresi yakalama
        match = re.search(r'([a-zA-Z0-9\.\-]+\.(?:ply\.gg|playit\.gg)(?::\d+)?)', msg)
        if match:
            self._on_address_found(match.group(1))
        
        m_ngrok = re.search(r'tcp://([a-zA-Z0-9\.\-]+:\d+)', msg)
        if m_ngrok:
            self._on_address_found(m_ngrok.group(1))

    def _on_address_found(self, addr):
        self.extracted_address = addr
        self.after(0, self._update_address_box, addr)

    def _update_address_box(self, addr):
        self.lbl_address.configure(state="normal")
        self.lbl_address.delete(0, "end")
        self.lbl_address.insert(0, addr)
        self.lbl_address.configure(state="readonly")

    def _copy_address(self):
        text = self.lbl_address.get()
        if "ornek" not in text and "belirecektir" not in text and text.strip():
            self.clipboard_clear()
            self.clipboard_append(text.strip())
            messagebox.showinfo("Kopyalandı", f"✅ Tünel bağlantı adresi panoya kopyalandı:\n\n{text.strip()}\n\nArkadaşlarınıza bu IP'yi gönderebilirsiniz!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir tünel başlatıp bağlantı adresinin oluşmasını bekleyiniz.")

    def _get_target_port(self):
        try:
            return int(self.port_var.get().strip())
        except Exception:
            return 25565

    def _start_playit(self):
        self.btn_playit.configure(state="disabled", text="⏳ Başlatılıyor...")
        def _worker():
            self.tunnel.start_playit()
            self.after(0, lambda: self.btn_playit.configure(state="normal", text="⚡ Playit.gg Başlat"))
        threading.Thread(target=_worker, daemon=True).start()

    def _start_cloudflare(self):
        port = self._get_target_port()
        self.btn_cf.configure(state="disabled", text="⏳ Başlatılıyor...")
        def _worker():
            self.tunnel.start_cloudflare(port=port)
            self.after(0, lambda: self.btn_cf.configure(state="normal", text="☁️ Cloudflare Tunnel"))
        threading.Thread(target=_worker, daemon=True).start()

    def _start_ngrok(self):
        port = self._get_target_port()
        token = self.ngrok_token_var.get().strip()
        if token:
            cfg = self.config_manager.get_server_config()
            cfg["ngrok_authtoken"] = token
            self.config_manager.save_server_config(cfg)

        self.btn_ngrok.configure(state="disabled", text="⏳ Başlatılıyor...")
        def _worker():
            self.tunnel.start_ngrok(port=port, authtoken=token)
            self.after(0, lambda: self.btn_ngrok.configure(state="normal", text="🚀 ngrok TCP Başlat"))
        threading.Thread(target=_worker, daemon=True).start()

    def _start_localtonet(self):
        port = self._get_target_port()
        self.btn_localtonet.configure(state="disabled", text="⏳ Başlatılıyor...")
        def _worker():
            self.tunnel.start_localtonet(port=port)
            self.after(0, lambda: self.btn_localtonet.configure(state="normal", text="🌐 Localtonet Başlat"))
        threading.Thread(target=_worker, daemon=True).start()

    def _stop_tunnel(self):
        self.tunnel.stop_tunnel()
        self.lbl_address.configure(state="normal")
        self.lbl_address.delete(0, "end")
        self.lbl_address.insert(0, "Tünel kapatıldı.")
        self.lbl_address.configure(state="readonly")
        messagebox.showinfo("Tünel", "Tünel servisi durduruldu.")

    def _test_upnp(self):
        port = self._get_target_port()
        self.btn_upnp.configure(state="disabled", text="⏳ Taranıyor...")
        def _worker():
            self.tunnel.try_upnp_port_forward(port)
            self.after(0, lambda: self.btn_upnp.configure(state="normal", text="📡 Modem UPnP Test Et"))
        threading.Thread(target=_worker, daemon=True).start()
