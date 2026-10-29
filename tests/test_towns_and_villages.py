import sys
SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import admin_panel

def test_towns_and_villages_categories():
    towns_cat = admin_panel.TABS_DATA.get("🏘️ DEV KASABALAR, KÖYLER & ŞEHİRLER", [])
    houses_cat = admin_panel.TABS_DATA.get("🏡 LÜKS EVLER & MALİKANELER", [])

    assert len(towns_cat) >= 10, f"Towns category has only {len(towns_cat)} items"
    assert len(houses_cat) >= 10, f"Houses category has only {len(houses_cat)} items"

    t_names = [x[0].upper() for x in towns_cat]
    assert any("KÖY" in n or "VILLAGE" in n for n in t_names), "Missing Village in towns"
    assert any("BATI" in n or "KASABA" in n for n in t_names), "Missing Western Town in towns"
    assert any("VİKİNG" in n or "VIKING" in n for n in t_names), "Missing Viking Town in towns"
    assert any("VAHA" in n or "ÇÖL" in n for n in t_names), "Missing Desert Oasis in towns"

    h_names = [x[0].upper().replace("İ", "I") for x in houses_cat]
    assert any("HOBBIT" in n for n in h_names), "Missing Hobbit House"
    assert any("MALIKANE" in n or "MANSION" in n for n in h_names), "Missing Mansion"
    assert any("ŞALE" in n or "SALE" in n or "DAĞ" in n or "DAG" in n for n in h_names), "Missing Mountain Chalet"
    assert any("BUNGALOV" in n or "MALDIV" in n for n in h_names), "Missing Maldives Bungalow"

    print("test_towns_and_villages_categories: PASS")

if __name__ == "__main__":
    try:
        test_towns_and_villages_categories()
    except Exception as e:
        print("test_towns_and_villages_categories: FAIL ->", e)
