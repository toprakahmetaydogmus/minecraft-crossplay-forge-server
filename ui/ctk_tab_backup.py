# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Tab: World Backup & Restore Manager
Autonomous backup creation with 1-click restore.
"""

import os
import threading
import customtkinter as ctk
from tkinter import messagebox

from ui.modern_theme import *
from core.backup_manager import BackupManager

class CTkTabBackup(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager
        sdir = self.config_manager.get_server_config().get("server_dir", os.path.join(os.getcwd(), "server"))
        self.backup_mgr = BackupManager(sdir, log_callback=self._on_log)

        self._build_ui()
        self._refresh_backups()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Üst Panel: Yedek Al Butonları
        top_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        top_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))

        t_inner = ctk.CTkFrame(top_card, fg_color="transparent")
        t_inner.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(t_inner, text="💾 DÜNYA VE SUNUCU YEDEKLEME MERKEZİ", font=FONT_SUBTITLE, text_color=COLOR_ACCENT_CYAN).pack(side="left")

        self.btn_backup = ctk.CTkButton(
            t_inner,
            text="⚡ ŞİMDİ YEDEK AL (.ZIP)",
            font=FONT_BOLD,
            fg_color=COLOR_ACCENT_GREEN,
            text_color="#000000",
            hover_color="#34d399",
            height=36,
            command=self._start_backup
        )
        self.btn_backup.pack(side="right", padx=(6, 0))

        btn_ref = ctk.CTkButton(
            t_inner,
            text="🔄 Yenile",
            font=FONT_SMALL,
            width=70,
            height=36,
            fg_color=COLOR_BG_CARD_HOVER,
            command=self._refresh_backups
        )
        btn_ref.pack(side="right")

        # Alt Panel: Mevcut Yedekler Listesi
        list_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        list_card.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        list_card.grid_columnconfigure(0, weight=1)
        list_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(list_card, text="📦 MEVCUT SUNUCU YEDEKLERİ", font=FONT_BOLD, text_color=COLOR_TEXT_MAIN).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 6))

        self.scroll_list = ctk.CTkScrollableFrame(list_card, fg_color="transparent")
        self.scroll_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def _refresh_backups(self):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        backups = self.backup_mgr.list_backups()
        if not backups:
            ctk.CTkLabel(self.scroll_list, text="Henüz alınmış bir yedek bulunmuyor. 'Şimdi Yedek Al' butonuna basarak ilk yedeğinizi oluşturabilirsiniz.", font=FONT_REGULAR, text_color=COLOR_TEXT_MUTED).pack(pady=20)
            return

        for b in backups:
            row = ctk.CTkFrame(self.scroll_list, fg_color=COLOR_BG_CARD_HOVER, corner_radius=8)
            row.pack(fill="x", padx=6, pady=4)

            info_f = ctk.CTkFrame(row, fg_color="transparent")
            info_f.pack(side="left", padx=12, pady=8)

            ctk.CTkLabel(info_f, text=f"📁 {b['filename']}", font=FONT_BOLD, text_color=COLOR_ACCENT_GOLD).pack(anchor="w")
            ctk.CTkLabel(info_f, text=f"Tarih: {b['date']} | Boyut: {b['size_mb']} MB", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED).pack(anchor="w")

            btn_res = ctk.CTkButton(
                row,
                text="↩️ Geri Yükle",
                font=FONT_SMALL,
                width=90,
                height=28,
                fg_color=COLOR_ACCENT_CYAN,
                text_color="#000000",
                command=lambda fname=b['filename']: self._restore_backup(fname)
            )
            btn_res.pack(side="right", padx=12)

    def _start_backup(self):
        self.btn_backup.configure(state="disabled", text="⏳ Yedekleniyor...")
        def _worker():
            ok = self.backup_mgr.create_backup()
            self.after(0, lambda: self.btn_backup.configure(state="normal", text="⚡ ŞİMDİ YEDEK AL (.ZIP)"))
            self.after(0, self._refresh_backups)
            if ok:
                self.after(0, messagebox.showinfo, "Yedekleme", "🎉 Sunucu dünyası ve ayarları başarıyla yedeklendi!")
            else:
                self.after(0, messagebox.showerror, "Hata", "Yedekleme oluşturulamadı.")
        threading.Thread(target=_worker, daemon=True).start()

    def _restore_backup(self, fname):
        if not messagebox.askyesno("Geri Yükleme Onayı", f"'{fname}' yedeğini geri yüklemek mevcut dünya dosyalarınızın üzerine yazacaktır.\n\nEmin misiniz?"):
            return
        def _worker():
            ok = self.backup_mgr.restore_backup(fname)
            if ok:
                self.after(0, messagebox.showinfo, "Geri Yükleme", "✅ Yedek başarıyla geri yüklendi!")
            else:
                self.after(0, messagebox.showerror, "Hata", "Geri yükleme sırasında hata oluştu.")
        threading.Thread(target=_worker, daemon=True).start()

    def _on_log(self, msg):
        pass
