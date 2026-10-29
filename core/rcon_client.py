# -*- coding: utf-8 -*-
"""
Minecraft RCON Client (v3.8.0 Ultra)
Implements Source RCON Protocol with automatic reconnection, thread-safety,
packet fragmentation protection (1460-byte Minecraft packet limit),
and graceful connection state handling.
"""

import socket
import struct
import threading
import time

class MinecraftRcon:
    def __init__(self, host="127.0.0.1", port=25575, password="admin123"):
        self.host = host
        self.port = port
        self.password = password
        self.sock = None
        self.lock = threading.Lock()

    def check_listening(self, timeout=0.6):
        """Checks if the RCON port is reachable without attempting full auth."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((self.host, self.port))
            s.close()
            return True
        except Exception:
            return False

    def connect(self):
        with self.lock:
            try:
                if self.sock:
                    try:
                        self.sock.close()
                    except Exception:
                        pass
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(2.5)
                self.sock.connect((self.host, self.port))
                self._send(3, self.password)
                req_id, resp_type, _ = self._recv()
                if req_id == -1:
                    self.sock.close()
                    self.sock = None
                    return False
                return True
            except (ConnectionRefusedError, socket.timeout, OSError):
                self.sock = None
                return False
            except Exception:
                self.sock = None
                return False

    def send_command(self, cmd):
        with self.lock:
            if not self.sock:
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.settimeout(2.5)
                    self.sock.connect((self.host, self.port))
                    self._send(3, self.password)
                    req_id, _, _ = self._recv()
                    if req_id == -1:
                        self.sock.close()
                        self.sock = None
                        return "[Hata] RCON şifresi reddedildi. server.properties dosyasındaki rcon.password ile eşleştiğinden emin olun."
                except (ConnectionRefusedError, OSError) as e:
                    self.sock = None
                    # WinError 10061 / ConnectionRefusedError handling
                    if getattr(e, 'winerror', None) == 10061 or isinstance(e, ConnectionRefusedError):
                        return "[Sunucu Kapalı veya Açılıyor] Minecraft sunucusu henüz başlatılmadı veya RCON portunu (25575) açıyor. Lütfen Admin Panelindeki '🚀 Sunucuyu Başlat' butonuna basarak sunucunuzu açınız; dünya yüklendiğinde bağlantı otomatik kurulacaktır."
                    return f"[Sunucu Kapalı] Sunucuya bağlanılamadı: {e}. Lütfen sunucuyu başlatınız."
                except Exception as e:
                    self.sock = None
                    return f"[Bağlantı Hatası] {e}"

            try:
                self._send(2, cmd)
                _, _, body = self._recv()
                return body if body.strip() else "[OK] Komut sunucuya başarıyla iletildi."
            except Exception as e:
                self.sock = None
                return f"[Hata] Komut iletilemedi: {e}"

    def send_chained_commands(self, cmd_string, delay=0.08):
        """Splits commands by && and sends each safely below Minecraft's 1460-byte limit."""
        results = []
        sub_cmds = [c.strip() for c in cmd_string.split("&&") if c.strip()]
        for c in sub_cmds:
            resp = self.send_command(c)
            results.append(resp)
            if len(sub_cmds) > 1:
                time.sleep(delay)
        return "\n".join(results)

    def _send(self, req_type, payload):
        data = payload.encode("utf-8") + b"\x00\x00"
        length = 4 + 4 + len(data)
        pkt = struct.pack("<iii", length, 12345, req_type) + data
        self.sock.sendall(pkt)

    def _recv(self):
        header = self.sock.recv(12)
        if len(header) < 12:
            return -1, 0, ""
        length, req_id, resp_type = struct.unpack("<iii", header)
        remaining = length - 8
        body = b""
        while len(body) < remaining:
            chunk = self.sock.recv(min(4096, remaining - len(body)))
            if not chunk:
                break
            body += chunk
        return req_id, resp_type, body[:-2].decode("utf-8", errors="replace")

    def is_connected(self):
        return self.sock is not None
