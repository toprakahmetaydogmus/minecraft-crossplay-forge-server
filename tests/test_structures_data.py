import sys
SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import admin_panel

def test_structures_count_and_variety():
    items = admin_panel.TABS_DATA.get("🏠 OTO İNŞAAT & EV YAPICI", [])
    assert len(items) >= 40, f"Yapı sayısı {len(items)}, en az 40 olmalı"
    names = [x[0] for x in items]
    assert any("Gökdelen" in n for n in names), "Missing Gökdelen"
    assert any("Katedral" in n for n in names), "Missing Katedral"
    assert any("Tapınak" in n or "Torii" in n for n in names), "Missing Tapınak/Torii"
    assert any("Banka" in n or "Kasa" in n for n in names), "Missing Banka"
    assert any("Stadyum" in n for n in names), "Missing Stadyum"
    assert any("Havalimanı" in n for n in names), "Missing Havalimanı"
    assert any("Kalyon" in n or "Gemi" in n for n in names), "Missing Kalyon/Gemi"

if __name__ == "__main__":
    try:
        test_structures_count_and_variety()
        print("test_structures_data: PASS")
    except AssertionError as e:
        print("test_structures_data: FAIL ->", e)
