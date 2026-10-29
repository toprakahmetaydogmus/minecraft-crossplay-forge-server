import ctypes
import os
import subprocess

# Win32 Process Priority Constants
IDLE_PRIORITY_CLASS = 0x00000040
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
NORMAL_PRIORITY_CLASS = 0x00000020
ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
HIGH_PRIORITY_CLASS = 0x00000080

PROCESS_SET_INFORMATION = 0x0200
PROCESS_QUERY_INFORMATION = 0x0400

kernel32 = ctypes.windll.kernel32

def set_process_priority(pid, priority_class):
    handle = kernel32.OpenProcess(PROCESS_SET_INFORMATION | PROCESS_QUERY_INFORMATION, False, pid)
    if handle:
        success = kernel32.SetPriorityClass(handle, priority_class)
        kernel32.CloseHandle(handle)
        return bool(success)
    return False

def get_pids_by_name(process_name):
    try:
        out = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}" /FO CSV /NH', shell=True, text=True)
        pids = []
        for line in out.strip().splitlines():
            parts = line.split('","')
            if len(parts) >= 2:
                pid_str = parts[1].replace('"', '')
                if pid_str.isdigit():
                    pids.append(int(pid_str))
        return pids
    except Exception:
        return []

# 1. CS2 -> HIGH PRIORITY
cs2_pids = get_pids_by_name("cs2.exe")
for pid in cs2_pids:
    ok = set_process_priority(pid, HIGH_PRIORITY_CLASS)
    print(f"CS2.exe (PID {pid}) Priority set to HIGH: {ok}")

# 2. Java (Minecraft Server) -> BELOW NORMAL (ensures zero stutters for CS2)
java_pids = get_pids_by_name("java.exe")
for pid in java_pids:
    ok = set_process_priority(pid, BELOW_NORMAL_PRIORITY_CLASS)
    print(f"Java.exe (PID {pid}) Priority set to BELOW_NORMAL: {ok}")

# 3. Python background tools -> IDLE
py_pids = get_pids_by_name("python.exe")
current_pid = os.getpid()
for pid in py_pids:
    if pid != current_pid:
        ok = set_process_priority(pid, IDLE_PRIORITY_CLASS)
        print(f"Python.exe (PID {pid}) Priority set to IDLE: {ok}")

print("Optimization complete!")
