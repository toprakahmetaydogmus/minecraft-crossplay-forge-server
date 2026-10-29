# -*- coding: utf-8 -*-
"""
Minecraft Crossplay Sunucusu Güvenli Kapatıcı (Graceful Stop)
Dünya verilerini diske yazar, oyuncuları güvenle kaydeder ve sunucuyu kapatır.
"""
import sys
import time
import socket
import struct
import os
import subprocess

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))

def get_server_rcon():
    host = os.environ.get("RCON_HOST", "127.0.0.1")
    port = int(os.environ.get("RCON_PORT", "25575"))
    password = os.environ.get("RCON_PASSWORD", "")

    props_file = os.path.join(SERVER_DIR, "server.properties")
    if os.path.exists(props_file):
        try:
            with open(props_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if k == "rcon.password" and not password:
                        password = v
                    elif k == "rcon.port" and "RCON_PORT" not in os.environ:
                        try:
                            port = int(v)
                        except ValueError:
                            pass
        except Exception:
            pass

    if not password:
        password = "AdminSecurePass123"

    return host, port, password

RCON_HOST, RCON_PORT, RCON_PASS = get_server_rcon()

def send_rcon_command(cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4.0)
        s.connect((RCON_HOST, RCON_PORT))

        def send_pkt(req_id, p_type, body):
            b_body = body.encode("utf-8")
            s.send(struct.pack("<iii", len(b_body) + 10, req_id, p_type) + b_body + b"\x00\x00")

        def recv_pkt():
            hdr = s.recv(12)
            if len(hdr) < 12:
                return -1, -1, ""
            length, req_id, p_type = struct.unpack("<iii", hdr)
            body = s.recv(length - 8)
            return req_id, p_type, body[:-2].decode("utf-8", errors="replace")

        send_pkt(1, 3, RCON_PASS)
        r_id, _, _ = recv_pkt()
        if r_id == -1:
            s.close()
            return False, "RCON Yetkilendirme hatası."

        send_pkt(2, 2, cmd)
        _, _, resp = recv_pkt()
        s.close()
        return True, resp
    except Exception as e:
        return False, str(e)

def main():
    print("=====================================================================")
    print("           MINECRAFT GÜVENLİ DÜNYA KAYDI VE KAPATICI")
    print("=====================================================================")
    print("[1/5] Sunucuya bağlantı kontrol ediliyor...")

    ok, resp = send_rcon_command("list")
    if not ok:
        print(f"[!] RCON bağlantısı kurulamadı: {resp}")
        print("[*] Sunucu zaten kapalı olabilir veya port meşgul.")
        return

    print(f"[*] Sunucu yanıtı: {resp.strip() if resp else 'Bağlantı başarılı'}")

    print("[2/5] Oyunculara kapatma duyurusu yapılıyor...")
    send_rcon_command('title @a title {"text":"⚠️ SUNUCU KAPANIYOR","color":"red","bold":true}')
    send_rcon_command('title @a subtitle {"text":"Tüm veriler kaydediliyor...","color":"gold"}')
    send_rcon_command("broadcast &8[&4Sunucu&8] &c&lSunucu bakim ve guvenli kapatma moduna girdi!")
    time.sleep(1.0)

    print("[3/5] Dünya ve envanter verileri diske kalıcı olarak kaydediliyor (Flush)...")
    send_rcon_command("save-all flush")
    time.sleep(1.5)

    print("[4/5] Oyuncular güvenle ana menüye aktarılıyor...")
    send_rcon_command("kick @a Sunucu guvenle kapatildi. Dunya kaydedildi.")
    time.sleep(0.5)

    print("[5/5] Sunucuya 'stop' komutu iletiliyor...")
    send_rcon_command("stop")
    print("[OK] Kapatma komutu iletildi. Sunucu dosyalarını kaydederek kapanıyor...")

if __name__ == "__main__":
    main()
