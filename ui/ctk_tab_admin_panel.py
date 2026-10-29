# -*- coding: utf-8 -*-
"""
Modern CustomTkinter Wrapper: Master Admin Panel & Universal Block Spawner Hub
Embeds the massive 380+ command suite seamlessly into the modern CustomTkinter layout.
"""

import customtkinter as ctk
from ui.tab_admin_panel import TabAdminPanel
from ui.modern_theme import *
from ui.theme import apply_global_theme

class CTkTabAdminPanel(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_manager = config_manager

        apply_global_theme(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Admin panelini modern container içine göm
        self.admin = TabAdminPanel(self, config_manager)
        self.admin.frame.grid(row=0, column=0, sticky="nsew")
