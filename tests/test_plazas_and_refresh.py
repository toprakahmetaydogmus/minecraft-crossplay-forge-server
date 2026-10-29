import sys
SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import tkinter as tk
import admin_panel

def test_plazas_category_exists_and_rich():
    # 1. Check dedicated plaza category or plaza items in structures
    plazas_cat = admin_panel.TABS_DATA.get("🏢 MEGA PLAZALAR & GÖKDELENLER", [])
    structures_cat = admin_panel.TABS_DATA.get("🏠 OTO İNŞAAT & EV YAPICI", [])
    
    assert len(plazas_cat) >= 12, f"Plazas category has only {len(plazas_cat)} items"
    names = [x[0].upper() for x in plazas_cat + structures_cat]
    assert any("PLAZA" in n for n in names), "Missing Plaza in names"
    assert any("AVM" in n or "ALIŞVERİŞ" in n for n in names), "Missing Shopping Mall Plaza"
    assert any("İKİZ" in n or "TWIN" in n for n in names), "Missing Twin Plaza Towers"
    assert any("FİNANS" in n or "BORSA" in n for n in names), "Missing Finance Plaza"
    assert any("OTEL" in n or "REZİDANS" in n for n in names), "Missing Hotel/Residence Plaza"
    print("test_plazas_category_exists_and_rich: PASS")

def test_right_side_refresh_mechanism():
    root = tk.Tk()
    root.withdraw()
    try:
        app = admin_panel.AdminGuiApp(root)
        
        # Test switching between categories refreshes the right pane immediately
        app.switch_category("🏢 MEGA PLAZALAR & GÖKDELENLER")
        cards1 = len(app.cards_frame.winfo_children())
        assert cards1 >= 12, f"Failed to render plaza cards on switch: {cards1}"
        
        app.switch_category("🎰 CASİNO & ŞANS OYUNLARI")
        cards2 = len(app.cards_frame.winfo_children())
        assert cards2 >= 20, f"Failed to render casino cards on switch: {cards2}"
        
        # Test that search doesn't block category switch
        app.search_var.set("nonexistent_query_xyz")
        app.switch_category("🏠 OTO İNŞAAT & EV YAPICI")
        # search_var should be reset on category switch so items appear
        cards3 = len(app.cards_frame.winfo_children())
        assert cards3 >= 20, f"Search blocked cards on category switch: {cards3}"
        
        print("test_right_side_refresh_mechanism: PASS")
    finally:
        root.destroy()

if __name__ == "__main__":
    try:
        test_plazas_category_exists_and_rich()
    except Exception as e:
        print("test_plazas_category_exists_and_rich: FAIL ->", e)

    try:
        test_right_side_refresh_mechanism()
    except Exception as e:
        print("test_right_side_refresh_mechanism: FAIL ->", e)
