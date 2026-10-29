import sys
SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import admin_panel

def test_casino_category_exists_and_rich():
    items = admin_panel.TABS_DATA.get("🎰 CASİNO & ŞANS OYUNLARI", [])
    assert len(items) >= 20, f"Casino items count is only {len(items)}"
    names = [x[0].upper() for x in items]
    assert any("SLOT" in n for n in names), "Missing Slot Makinesi"
    assert any("RULET" in n for n in names), "Missing Rulet"
    assert any("BLACKJACK" in n or "21" in n for n in names), "Missing Blackjack"
    assert any("YAZI" in n or "ZAR" in n for n in names), "Missing Coinflip/Dice"
    assert any("CASİNO" in n or "KUMARHANE" in n for n in names), "Missing Casino Palace"

if __name__ == "__main__":
    try:
        test_casino_category_exists_and_rich()
        print("test_casino_data: PASS")
    except AssertionError as e:
        print("test_casino_data: FAIL ->", e)
