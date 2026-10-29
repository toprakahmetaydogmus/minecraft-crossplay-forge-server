import sys
import os

SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import tkinter as tk
import admin_panel

def test_admin_gui_initialization():
    root = tk.Tk()
    root.withdraw()
    try:
        app = admin_panel.AdminGuiApp(root)
        assert hasattr(app, "sidebar_canvas"), "Missing sidebar_canvas"
        assert hasattr(app, "content_canvas"), "Missing content_canvas"
        assert hasattr(app, "selected_category"), "Missing selected_category"
        assert len(app.category_buttons) >= 20, f"Only {len(app.category_buttons)} category buttons"
        assert app.cols in [1, 2, 3], f"Invalid cols: {app.cols}"
        print("test_panel_ui: PASS")
    finally:
        root.destroy()

if __name__ == "__main__":
    try:
        test_admin_gui_initialization()
    except Exception as e:
        print("test_panel_ui: FAIL ->", e)
