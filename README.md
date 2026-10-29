<div align="center">

# ⚔️ Minecraft Crossplay Forge 1.20.1 & Ultimate Admin Panel
### **The Next-Generation Minecraft Server Suite with 40+ Admin Panels, 160+ Instant Structures & Java-Bedrock Crossplay**

[![GitHub Stars](https://img.shields.io/github/stars/toprakahmetaydogmus/minecraft-crossplay-forge-server?style=for-the-badge&logo=github&color=gold)](https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server/stargazers)
[![Minecraft Version](https://img.shields.io/badge/Minecraft-1.20.1-brightgreen?style=for-the-badge&logo=minecraft)](https://www.minecraft.net/)
[![Forge Version](https://img.shields.io/badge/Forge-47.2.20-orange?style=for-the-badge)](https://files.minecraftforge.net/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)
[![Crossplay](https://img.shields.io/badge/Crossplay-Java%20%2B%20Bedrock-cyan?style=for-the-badge)](https://geysermc.org/)

<br/>

> **🚀 If you like this project, please consider giving it a ⭐ Star on GitHub!**  
> [![Star on GitHub](https://img.shields.io/badge/⭐%20Star%20This%20Repo-Gold?style=for-the-badge)](https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server)

[🇹🇷 Türkçe Dokümantasyon İçin Tıklayın (README_TR.md)](README_TR.md)

</div>

---

## 🌟 Why Choose This Server Suite?

Setting up a high-performance modded Minecraft server with cross-platform support and an advanced management interface usually takes hours of frustrating configuration. 

**This project solves that in under 2 minutes.** Even a complete beginner can clone the repo, run a single setup script, and immediately enjoy a fully loaded Minecraft Forge 1.20.1 server with Java and Bedrock crossplay, 160+ instant structures, and an advanced graphical Admin Panel.

---

## ✨ Key Features

### 🏛️ 1. Schematics Studio & rom1504 Dataset Architecture
- **160+ Instant Structures**: Modern luxury villas, medieval stone castles, mountain chalets, skyscrapers, underground bunkers, redstone automated farms, arenas, and historical landmarks.
- **Dataset Integration**: Inspired by the [`rom1504/minecraft-schematics-dataset`](https://github.com/rom1504/minecraft-schematics-dataset) structure format.
- **Advanced Controls**:
  - 🔄 **Rotation**: 0°, 90°, 180°, 270°.
  - 🪞 **Mirroring**: None, Left-to-Right, Front-to-Back.
  - 🎯 **Targeting**: Relative to Player (`~ ~ ~`) or Exact World XYZ coordinates.
  - 🧹 **Auto-Clear Ground & Air**: Clears foliage and trees automatically before building.
  - ↩️ **1-Click Undo Engine**: Instantly revert placed structures block-by-block if misplaced.
  - 📂 **Local `.schem` & `.nbt` File Importer**: Load any schematic directly into your world.

### 🎮 2. Java & Bedrock Crossplay Out of the Box
- **GeyserMC & Floodgate**: Seamless connection for PC (Java), iOS, Android, Nintendo Switch, Xbox, and PlayStation.
- **Default Ports**:
  - **Java Edition**: `25565` (TCP)
  - **Bedrock Edition**: `19132` (UDP)
  - **RCON Management**: `25575` (TCP)

### 🎛️ 3. Ultimate Cyberpunk Admin Panel (40+ Categories)
- **High-Speed Thread-Safe RCON**: Instant command execution and automatic reconnect.
- **Live Server Console**: Real-time log monitoring with interactive syntax highlighting.
- **One-Click Actions**:
  - 💰 **Economy & Banking**: Real-time scoreboards, physical currency, periodic salary dispenser.
  - 🏪 **Custom NPC Grand Bazaar**: 6 specialized merchant trades (Blacksmith, Enchanter, Alchemist, etc.).
  - ⚡ **32k God Items**: Level 255 enchanted weapons, apocalypse blades, unbreakable shields.
  - 🎪 **Server Minigames & Boss Events**: Meteor showers, gold storms, Wither & Warden arena spawners.
  - 🤡 **Troll & Player Moderation**: Freeze, cage, launch rocket, drop anvils, reset inventories.
  - 🧹 **Anti-Lag & Performance Watchdog**: Real-time entity wiper, TPS booster, gamerule shield.

### 🛡️ 4. Zero-Leak Security & Privacy Architecture
- **No Hardcoded IPs**: Local network interfaces and tunnels are never exposed or committed.
- **Dynamic Credentials**: RCON passwords and ports are dynamically read from `server.properties` or environment variables (`.env`).
- **Comprehensive `.gitignore`**: All personal player UUIDs, logs, databases, and world save files are strictly ignored.

---

## ⚡ 2-Minute Quick Start Guide

### 🪟 Windows Setup
```bat
# 1. Clone the repository
git clone https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server.git
cd minecraft-crossplay-forge-server

# 2. Run the 2-Minute Installer
setup_server.bat
```
*The installer automatically validates Java 17+, downloads the Arclight core jar, installs required Python libraries (`nbtlib`, `requests`), sets up EULA, and launches the server and Admin Panel!*

To launch both the server and admin panel anytime:
```bat
START_ALL.bat
```

---

### 🐧 Linux / macOS Setup
```bash
# 1. Clone the repository
git clone https://github.com/toprakahmetaydogmus/minecraft-crossplay-forge-server.git
cd minecraft-crossplay-forge-server

# 2. Run the installer
chmod +x setup_server.sh
./setup_server.sh

# 3. Launch the server and Admin Panel
./run.sh
python3 admin_panel.py
```

---

## 📁 Repository Architecture

```text
├── admin_panel.py            # Master GUI Admin Panel (40+ Categories, RCON Client)
├── schematics_manager.py     # Schematics Studio & rom1504 Dataset Engine (160+ presets)
├── schematics/               # Storage directory for .schem and .nbt structure files
├── build_plugin.py           # Source code for Vault + Scoreboard Economy Sync plugin
├── graceful_stop.py          # Graceful world flusher and server stopper
├── setup_server.bat          # 2-minute automated Windows setup wizard
├── setup_server.sh           # 2-minute automated Linux/macOS setup wizard
├── START_ALL.bat             # 1-Click launcher for both Server and Admin Panel
├── ADMIN_PANEL.bat           # Desktop shortcut launcher for the GUI
├── start.bat                 # Server launch script with auto-RAM tuning
├── setup_firewall.bat        # Windows Firewall port rule configurator (25565 & 19132)
├── server.properties.example # Documented server configuration template
├── ops.example.json          # Example OP operator permissions file
├── .env.example              # Environment variables template
├── mods/                     # Forge 1.20.1 Mods (FerriteCore, MouseTweaks, JEI, AntiXray)
└── plugins/                  # Spigot/Paper Plugins (Geyser, TAB, EssentialsX, EconomyShop)
```

---

## 🛠️ Mods & Plugins Included

| Component | Type | Function |
|---|---|---|
| **Arclight Forge 1.20.1** | Hybrid Core | Runs Forge mods and Bukkit/Spigot/Paper plugins together |
| **Geyser-Spigot & Floodgate** | Plugin | Enables Minecraft Bedrock players to join Java servers |
| **Just Enough Items (JEI)** | Mod | In-game recipe and item viewer (Forge 1.20.1) |
| **Mouse Tweaks** | Mod | Enhanced inventory and crafting item management |
| **FerriteCore** | Mod | Drastically reduces Minecraft server memory (RAM) usage |
| **TAB** | Plugin | Animated scoreboard, tablist, and player nametags |
| **EssentialsX** | Plugin | Warps, homes, kits, spawn, and teleports |
| **EconomyShopGUI & Vault** | Plugin | Full dynamic player economy and GUI bazaar |
| **GrimAC** | Plugin | Next-generation packet-level anti-cheat protection |

---

## 🎮 Admin Commands Cheatsheet

| Action | Minecraft In-Game Command |
|---|---|
| **Instant Creative Mode** | `/gamemode creative` |
| **Save World Data (Flush)** | `/save-all flush` |
| **Clean All Ground Lag** | `/kill @e[type=item]` |
| **Give Player 50,000 Currency** | `/scoreboard players add <player> akce 50000` |
| **Open Economy Market** | `/shop` or `/n` |
| **Claim Land with Golden Shovel** | `/arsa` or `/claim` |
| **Safe Player Trade** | `/takas <player>` or `/trade <player>` |

---

## 🤝 Contributing & Stargazers

Contributions, suggestions, and pull requests are warmly welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Don't forget to **⭐ Star** this repository if you find it helpful!

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for more information.
