# -*- coding: utf-8 -*-
"""
Modern Cyberpunk / Deep Slate Theme Tokens
"""

import tkinter as tk
from tkinter import ttk

BG_DARK = "#080c14"
BG_PANEL = "#0c1220"
BG_CARD = "#111a2e"
BG_HOVER = "#18243f"
BORDER_COLOR = "#1e2e4e"
TEXT_COLOR = "#ffffff"
TEXT_MUTED = "#94a3b8"

ACCENT_CYAN = "#00d2ff"
ACCENT_GREEN = "#00f090"
ACCENT_GOLD = "#ffb800"
ACCENT_PURPLE = "#a855f7"
ACCENT_RED = "#ff3b5c"

def apply_global_theme(root):
    try:
        root.configure(bg=BG_DARK)
    except Exception:
        pass
    try:
        style = ttk.Style()
        style.theme_use("clam")

        # Notebook Tabs
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_COLOR,
                        padding=[14, 7], font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT_CYAN), ("active", BG_HOVER)],
                  foreground=[("selected", "#000000"), ("active", "#ffffff")])

        # Comboboxes
        style.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD,
                        foreground=TEXT_COLOR, arrowcolor=ACCENT_CYAN, borderwidth=0)

        # Progressbar
        style.configure("Horizontal.TProgressbar", background=ACCENT_CYAN, troughcolor=BG_CARD, borderwidth=0)
    except Exception:
        pass
