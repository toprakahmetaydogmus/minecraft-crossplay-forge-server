# -*- coding: utf-8 -*-
"""
Live Hardware & Server Performance Monitor
Provides real-time telemetry for CPU, RAM, Disk, and Java process utilization.
"""

import os
import psutil

class HardwareMonitor:
    @staticmethod
    def get_system_metrics():
        """Returns system CPU, RAM, and Disk metrics."""
        try:
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(os.getcwd())

            return {
                "cpu_percent": cpu_pct,
                "ram_percent": mem.percent,
                "ram_used_gb": round(mem.used / (1024**3), 2),
                "ram_total_gb": round(mem.total / (1024**3), 2),
                "ram_free_gb": round(mem.available / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 1)
            }
        except Exception:
            return {
                "cpu_percent": 0,
                "ram_percent": 0,
                "ram_used_gb": 0,
                "ram_total_gb": 8,
                "ram_free_gb": 4,
                "disk_free_gb": 50
            }

    @staticmethod
    def find_minecraft_process(server_dir=None):
        """Finds running java process hosting the Minecraft server."""
        try:
            norm_sdir = os.path.abspath(server_dir).lower() if server_dir else None
            for p in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'cpu_percent']):
                try:
                    pname = p.info.get('name', '').lower()
                    if 'java' in pname:
                        cmdline = ' '.join(p.info.get('cmdline') or []).lower()
                        if norm_sdir and norm_sdir in cmdline:
                            return p
                        elif 'minecraft' in cmdline or 'nogui' in cmdline or 'paper' in cmdline or 'forge' in cmdline:
                            return p
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
        return None

    @staticmethod
    def get_server_process_metrics(server_dir=None):
        """Returns metrics for the running Minecraft server process."""
        proc = HardwareMonitor.find_minecraft_process(server_dir)
        if not proc:
            return {"running": False, "pid": None, "ram_mb": 0, "cpu_pct": 0}

        try:
            mem_info = proc.memory_info()
            ram_mb = round(mem_info.rss / (1024 * 1024), 1)
            cpu = proc.cpu_percent(interval=None)
            return {
                "running": True,
                "pid": proc.pid,
                "ram_mb": ram_mb,
                "cpu_pct": cpu
            }
        except Exception:
            return {"running": False, "pid": None, "ram_mb": 0, "cpu_pct": 0}
