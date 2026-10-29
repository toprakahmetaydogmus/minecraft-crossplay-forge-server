import os
import sys

SERVER_DIR = r"C:\Users\topra_n3vq63d\.gemini\antigravity-ide\scratch\minecraft_crossplay_forge_server"

def test_antixray_toml():
    cfg_path = os.path.join(SERVER_DIR, "config", "antixray.toml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "enabled = true" in content or "enabled=true" in content, "Global enabled must be true"
    assert "engineMode = 2" in content or "engineMode=2" in content, "engineMode must be 2 (OBFUSCATE)"
    assert "maxBlockHeight = 320" in content, "maxBlockHeight must be 320 for 1.20.1"
    assert "diamond_ore" in content or "#forge:ores" in content, "diamond_ore or #forge:ores must be hidden"

def test_spigot_antixray():
    spigot_path = os.path.join(SERVER_DIR, "spigot.yml")
    with open(spigot_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "enabled: true" in content, "Spigot anti-xray must be enabled"
    assert "engine-mode: 2" in content, "Spigot anti-xray engine-mode must be 2"
    assert "max-block-height: 320" in content, "Spigot max-block-height must be 320"

if __name__ == "__main__":
    try:
        test_antixray_toml()
        print("test_antixray_toml: PASS")
    except AssertionError as e:
        print("test_antixray_toml: FAIL ->", e)

    try:
        test_spigot_antixray()
        print("test_spigot_antixray: PASS")
    except AssertionError as e:
        print("test_spigot_antixray: FAIL ->", e)
