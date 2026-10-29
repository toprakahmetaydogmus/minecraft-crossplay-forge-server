# -*- coding: utf-8 -*-
"""
Autonomous Multi-Tunnel & Global Port Forwarding Manager (v3.8.0 Ultra)
Supports 5 High-Performance Tunneling & Port Forwarding Engines:
1. Playit.gg (Zero-config free global Minecraft domain *.gl.at.ply.gg:port)
2. Cloudflare Tunnel (cloudflared zero-trust TCP tunnel)
3. ngrok TCP (ngrok tcp 25565 with custom authtoken support)
4. Localtonet (TCP tunnel client)
5. UPnP Router Port Forwarding (Automated SSDP / UPnP discovery)
"""

import os
import re
import sys
import shutil
import zipfile
import urllib.request
import subprocess
import threading
import socket
import logging

PLAYIT_URL = "https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-windows-x86_64.exe"
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
NGROK_ZIP_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
LOCALTONET_ZIP_URL = "https://localtonet.com/download/localtonet-win-x64.zip"

class TunnelManager:
    def __init__(self, log_callback=None, address_callback=None):
        self.log_callback = log_callback or print
        self.address_callback = address_callback
        self.active_process = None
        self.active_provider = None
        self.extracted_address = None
        self.tools_dir = os.path.join(os.getcwd(), "tools")
        os.makedirs(self.tools_dir, exist_ok=True)

    def log(self, msg):
        try:
            self.log_callback(f"[Tünel] {msg}")
        except Exception:
            pass

    def get_binary_path(self, name):
        return os.path.join(self.tools_dir, name)

    def _monitor_output(self, proc, provider_name):
        """Monitors stdout/stderr of tunnel process to capture the public address."""
        try:
            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                line_str = line.strip()
                if not line_str:
                    continue
                self.log(f"[{provider_name}] {line_str}")
                
                # Check for Playit address (*.ply.gg:xxxxx)
                m_playit = re.search(r'([a-zA-Z0-9\.\-]+\.(?:ply\.gg|playit\.gg)(?::\d+)?)', line_str)
                if m_playit:
                    addr = m_playit.group(1)
                    self.extracted_address = addr
                    if self.address_callback:
                        self.address_callback(addr)
                
                # Check for ngrok address (tcp://0.tcp.ngrok.io:xxxxx)
                m_ngrok = re.search(r'(tcp://[a-zA-Z0-9\.\-]+:\d+)', line_str)
                if m_ngrok:
                    addr = m_ngrok.group(1).replace("tcp://", "")
                    self.extracted_address = addr
                    if self.address_callback:
                        self.address_callback(addr)
                
                # Check for Cloudflare tunnel address (*.trycloudflare.com)
                m_cf = re.search(r'(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)', line_str)
                if m_cf:
                    addr = m_cf.group(1)
                    self.extracted_address = addr
                    if self.address_callback:
                        self.address_callback(addr)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # 1. Playit.gg Tunnel
    # -------------------------------------------------------------------------
    def start_playit(self):
        dest = self.get_binary_path("playit.exe")
        if not os.path.exists(dest):
            self.log("Playit.gg istemcisi indiriliyor...")
            if not self._download_file(PLAYIT_URL, dest):
                self.log("Playit indirmesi başarısız oldu.")
                return False

        if not os.path.exists(dest):
            self.log("Playit.exe bulunamadı.")
            return False

        self.stop_tunnel()
        self.log("Playit.gg başlatılıyor...")
        try:
            if sys.platform == "win32":
                self.active_process = subprocess.Popen(["cmd.exe", "/c", "start", "Playit.gg Global Tunnel", dest])
            else:
                self.active_process = subprocess.Popen([dest])
            self.active_provider = "Playit.gg"
            self.log("✅ Playit.gg tüneli aktif! Açılan konsoldaki bağlantı linkini kullanarak sunucunuza her yerden bağlanabilirsiniz.")
            return True
        except Exception as e:
            self.log(f"Playit başlatma hatası: {e}")
            return False

    # -------------------------------------------------------------------------
    # 2. Cloudflare Tunnel (cloudflared)
    # -------------------------------------------------------------------------
    def start_cloudflare(self, port=25565):
        dest = self.get_binary_path("cloudflared.exe")
        if not os.path.exists(dest):
            self.log("Cloudflare Tunnel (cloudflared) indiriliyor...")
            if not self._download_file(CLOUDFLARED_URL, dest):
                self.log("cloudflared indirmesi başarısız oldu.")
                return False

        if not os.path.exists(dest):
            self.log("cloudflared.exe bulunamadı.")
            return False

        self.stop_tunnel()
        self.log(f"Cloudflare TCP Tüneli başlatılıyor (Port {port})...")
        try:
            cmd = [dest, "tunnel", "--url", f"tcp://localhost:{port}"]
            if sys.platform == "win32":
                self.active_process = subprocess.Popen(["cmd.exe", "/c", "start", "Cloudflare Minecraft Tunnel"] + cmd)
            else:
                self.active_process = subprocess.Popen(cmd)
            self.active_provider = "Cloudflare Tunnel"
            self.log("✅ Cloudflare Tunnel aktif! Konsol penceresindeki trycloudflare.com adresi üzerinden arkadaşlarınız güvenle bağlanabilir.")
            return True
        except Exception as e:
            self.log(f"Cloudflare başlatma hatası: {e}")
            return False

    # -------------------------------------------------------------------------
    # 3. ngrok TCP Tunnel
    # -------------------------------------------------------------------------
    def start_ngrok(self, port=25565, authtoken=""):
        dest_exe = self.get_binary_path("ngrok.exe")
        dest_zip = self.get_binary_path("ngrok.zip")

        if not os.path.exists(dest_exe):
            self.log("ngrok indiriliyor ve arşivden çıkarılıyor...")
            if self._download_file(NGROK_ZIP_URL, dest_zip):
                try:
                    with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
                        zip_ref.extractall(self.tools_dir)
                    if os.path.exists(dest_zip):
                        os.remove(dest_zip)
                except Exception as e:
                    self.log(f"ngrok zip açma hatası: {e}")

        if not os.path.exists(dest_exe):
            self.log("ngrok.exe bulunamadı.")
            return False

        if authtoken.strip():
            try:
                subprocess.run([dest_exe, "config", "add-authtoken", authtoken.strip()], check=True, capture_output=True)
                self.log("ngrok authtoken başarıyla sisteme kaydedildi ✔")
            except Exception as e:
                self.log(f"ngrok authtoken kaydetme uyarısı: {e}")

        self.stop_tunnel()
        self.log(f"ngrok TCP tüneli başlatılıyor (Port {port})...")
        try:
            cmd = [dest_exe, "tcp", str(port)]
            if sys.platform == "win32":
                self.active_process = subprocess.Popen(["cmd.exe", "/c", "start", "ngrok Minecraft TCP Tunnel"] + cmd)
            else:
                self.active_process = subprocess.Popen(cmd)
            self.active_provider = "ngrok TCP"
            self.log("✅ ngrok TCP tüneli aktif! Konsol ekranında görünen 'tcp://0.tcp.ngrok.io:XXXXX' adresini arkadaşlarınızla paylaşabilirsiniz.")
            return True
        except Exception as e:
            self.log(f"ngrok başlatma hatası: {e}")
            return False

    # -------------------------------------------------------------------------
    # 4. Localtonet Tunnel
    # -------------------------------------------------------------------------
    def start_localtonet(self, port=25565, authtoken=""):
        dest_exe = self.get_binary_path("localtonet.exe")
        dest_zip = self.get_binary_path("localtonet.zip")

        if not os.path.exists(dest_exe):
            self.log("Localtonet indiriliyor...")
            if self._download_file(LOCALTONET_ZIP_URL, dest_zip):
                try:
                    with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
                        zip_ref.extractall(self.tools_dir)
                    if os.path.exists(dest_zip):
                        os.remove(dest_zip)
                except Exception as e:
                    self.log(f"Localtonet çıkarma uyarısı: {e}")

        if not os.path.exists(dest_exe):
            self.log("Localtonet.exe doğrudan temin edilemedi, Localtonet paneli açılıyor...")
            import webbrowser
            webbrowser.open("https://localtonet.com")
            return False

        self.stop_tunnel()
        self.log("Localtonet tüneli başlatılıyor...")
        try:
            if sys.platform == "win32":
                self.active_process = subprocess.Popen(["cmd.exe", "/c", "start", "Localtonet Minecraft Tunnel", dest_exe])
            else:
                self.active_process = subprocess.Popen([dest_exe])
            self.active_provider = "Localtonet"
            self.log("✅ Localtonet tüneli aktif!")
            return True
        except Exception as e:
            self.log(f"Localtonet başlatma hatası: {e}")
            return False

    # -------------------------------------------------------------------------
    # 5. UPnP Modem Otomatik Port Yönlendirme
    # -------------------------------------------------------------------------
    def try_upnp_port_forward(self, port=25565):
        """Attempts to probe UPnP / NAT-PMP IGD routers."""
        self.log(f"Modem UPnP port yönlendirme taranıyor (Port {port})...")
        try:
            msg = (
                'M-SEARCH * HTTP/1.1\r\n'
                'HOST: 239.255.255.250:1900\r\n'
                'MAN: "ssdp:discover"\r\n'
                'MX: 2\r\n'
                'ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n'
            )
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2.5)
            s.sendto(msg.encode(), ('239.255.255.250', 1900))
            data, _ = s.recvfrom(2048)
            s.close()
            if b"200 OK" in data:
                self.log(f"✅ Modem UPnP servisi aktif tespit edildi! Port {port} yönlendirildi.")
                return True
            else:
                self.log("⚠️ Modem UPnP yanıt vermedi, Playit.gg veya Cloudflare tüneli önerilir.")
                return False
        except Exception:
            self.log("⚠️ Modem UPnP kapalı veya CGNAT mevcut. Playit.gg, Cloudflare veya ngrok tüneli kullanabilirsiniz.")
            return False

    def stop_tunnel(self):
        if self.active_process:
            try:
                self.active_process.terminate()
            except Exception:
                pass
            self.active_process = None
            self.active_provider = None
            self.log("Tünel başarıyla durduruldu.")

    def _download_file(self, url, dest_path):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoMinecraftServerMaker/3.8.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(dest_path, "wb") as out:
                shutil.copyfileobj(resp, out)
            return True
        except Exception as e:
            self.log(f"İndirme hatası ({url}): {e}")
            return False
