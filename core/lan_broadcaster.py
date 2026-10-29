# -*- coding: utf-8 -*-
"""
Multi-Adapter LAN Broadcaster
Broadcasts Minecraft LAN discovery packets (224.0.2.60:4445) across all
available IPv4 network adapters (WiFi, Ethernet, VPN, Radmin, Hamachi, ZeroTier).
"""

import socket
import threading
import time

class LanBroadcaster:
    def __init__(self, port=25565, motd="Auto Minecraft Server"):
        self.port = port
        self.motd = motd
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _worker(self):
        payload = f"[MOTD]\u00a76\u00a7l{self.motd}\u00a7f - \u00a7aAktif[/MOTD][AD]{self.port}[/AD]".encode("utf-8")
        while self.running:
            # Check if server port is actually open
            is_open = False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                res = s.connect_ex(("127.0.0.1", self.port))
                s.close()
                is_open = (res == 0)
            except Exception:
                is_open = False

            if is_open:
                interfaces = self._get_local_ips()
                for iface_ip in interfaces:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
                        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(iface_ip))
                        sock.sendto(payload, ("224.0.2.60", 4445))
                        sock.sendto(payload, ("255.255.255.255", 4445))
                        sock.close()
                    except Exception:
                        pass
            time.sleep(1.5)

    def _get_local_ips(self):
        ips = ["127.0.0.1"]
        try:
            hostname = socket.gethostname()
            for ip in socket.gethostbyname_ex(hostname)[2]:
                if not ip.startswith("127."):
                    ips.append(ip)
        except Exception:
            pass
        return ips
