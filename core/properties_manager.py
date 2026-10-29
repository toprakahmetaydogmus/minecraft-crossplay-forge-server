# -*- coding: utf-8 -*-
"""
Visual Server Properties Manager
Reads and writes Minecraft server.properties with safe key-value preservation.
"""

import os

DEFAULT_PROPERTIES = {
    "server-port": "25565",
    "enable-rcon": "true",
    "rcon.port": "25575",
    "rcon.password": "admin123",
    "online-mode": "false",
    "motd": "\\u00a76\\u00a7lAuto Minecraft Server\\u00a7f - \\u00a7aAktif!",
    "max-players": "20",
    "view-distance": "10",
    "simulation-distance": "8",
    "gamemode": "survival",
    "difficulty": "normal",
    "pvp": "true",
    "hardcore": "false",
    "enable-command-block": "true",
    "allow-flight": "true",
    "spawn-protection": "0",
    "white-list": "false"
}

class PropertiesManager:
    def __init__(self, server_dir):
        self.server_dir = os.path.abspath(server_dir)
        self.props_path = os.path.join(self.server_dir, "server.properties")

    def read_properties(self):
        """Reads server.properties into a dictionary."""
        props = dict(DEFAULT_PROPERTIES)
        if not os.path.exists(self.props_path):
            return props

        try:
            with open(self.props_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        props[k.strip()] = v.strip()
        except Exception:
            pass
        return props

    def save_properties(self, new_props):
        """Saves dictionary back to server.properties preserving valid keys."""
        os.makedirs(self.server_dir, exist_ok=True)
        # Read existing file to preserve comments if any
        lines = []
        written_keys = set()
        if os.path.exists(self.props_path):
            try:
                with open(self.props_path, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        stripped = line.strip()
                        if stripped.startswith("#"):
                            lines.append(line)
                        elif "=" in stripped:
                            k, _ = stripped.split("=", 1)
                            k = k.strip()
                            if k in new_props:
                                lines.append(f"{k}={new_props[k]}\n")
                                written_keys.add(k)
                            else:
                                lines.append(line)
            except Exception:
                pass

        # Append remaining keys
        for k, v in new_props.items():
            if k not in written_keys:
                lines.append(f"{k}={v}\n")

        with open(self.props_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
