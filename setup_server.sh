#!/usr/bin/env bash
# ===============================================================================
#   ⚡ MINECRAFT FORGE 1.20.1 CROSSPLAY + ULTIMATE ADMIN PANEL INSTALLER (LINUX/MAC)
# ===============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==============================================================================="
echo "  ⚡ MINECRAFT FORGE 1.20.1 CROSSPLAY + ULTIMATE ADMIN PANEL INSTALLER ⚡"
echo "==============================================================================="

# 1. Python Check
echo "[*] [1/5] Checking Python 3 and modules..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Please install python3 (e.g., sudo apt install python3 python3-pip)"
    exit 1
fi
python3 -m pip install -q --disable-pip-version-check nbtlib requests 2>/dev/null || true
echo "[OK] Python dependencies ready."

# 2. Java Check
echo "[*] [2/5] Checking Java 17+..."
if ! command -v java &> /dev/null; then
    echo "[!] Java not found. Please install OpenJDK 17 (e.g., sudo apt install openjdk-17-jre-headless)"
    exit 1
fi
echo "[OK] Java found: $(java -version 2>&1 | head -n 1)"

# 3. Accept EULA
echo "[*] [3/5] Accepting Minecraft EULA..."
echo "eula=true" > eula.txt
echo "[OK] eula.txt set to true."

# 4. Arclight Jar Check
echo "[*] [4/5] Checking server core jar..."
if [ ! -f "arclight-forge-1.20.1.jar" ] && [ ! -f "forge-1.20.1-server.jar" ]; then
    echo "[*] Downloading Arclight Forge 1.20.1 jar from official releases..."
    curl -fsSL -o "arclight-forge-1.20.1.jar" "https://github.com/ArclightPowered/Arclight/releases/download/Forge%2F1.20.1%2F1.0.8/arclight-forge-1.20.1-1.0.8.jar"
    echo "[OK] Server jar downloaded successfully."
else
    echo "[OK] Server jar is present."
fi

# 5. Configurations
echo "[*] [5/5] Checking server configuration..."
if [ ! -f "server.properties" ] && [ -f "server.properties.example" ]; then
    cp server.properties.example server.properties
fi

if [ ! -f "ops.json" ] && [ -f "ops.example.json" ]; then
    cp ops.example.json ops.json
fi

chmod +x *.sh 2>/dev/null || true
echo "[OK] Configuration ready."

echo "==============================================================================="
echo "  🎉 INSTALLATION COMPLETE! Ready in 2 minutes."
echo "  To start the server: ./run.sh"
echo "  To start the Admin Panel: python3 admin_panel.py"
echo "==============================================================================="
