import sys
import os

SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

import admin_panel

def test_desktop_batch_files():
    desktop_files = [
        r"C:\Users\topra_n3vq63d\OneDrive\Desktop\ADMIN_PANEL.bat",
        r"C:\Users\topra_n3vq63d\OneDrive\Desktop\SUNUCUYU_BASLAT.bat",
        r"C:\Users\topra_n3vq63d\OneDrive\Desktop\SUNUCUYU_KAPAT.bat",
        r"C:\Users\topra_n3vq63d\OneDrive\Desktop\RADMIN_BAGLANTI_DUZELTICI.bat"
    ]
    for bf in desktop_files:
        assert os.path.isfile(bf), f"Batch file not found: {bf}"

def test_command_templates_validity():
    total_commands = 0
    for cat_name, items in admin_panel.TABS_DATA.items():
        for btn_name, cmd_tmpl, desc in items:
            total_commands += 1
            # Check format with test target
            try:
                formatted = cmd_tmpl.replace("{p}", "TestPlayer")
                assert len(formatted) > 0
            except Exception as e:
                raise AssertionError(f"Invalid format in [{cat_name}] -> {btn_name}: {e}")

    assert total_commands >= 250, f"Total commands {total_commands} is too low"
    print(f"Verified {total_commands} command templates successfully.")

def test_rcon_live_connection():
    rcon = admin_panel.MinecraftRcon()
    res = rcon.send_command("list")
    assert "çevrimiçi" in res or "online" in res or "MIRKUNDAKLAYAN" in res or "players" in res.lower(), f"RCON output unexpected: {res}"
    print(f"RCON live test verified: {res.strip()[:60]}...")

if __name__ == "__main__":
    test_desktop_batch_files()
    print("test_desktop_batch_files: PASS")
    test_command_templates_validity()
    print("test_command_templates_validity: PASS")
    test_rcon_live_connection()
    print("test_rcon_live_connection: PASS")
