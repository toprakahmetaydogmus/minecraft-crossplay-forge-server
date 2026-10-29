import subprocess
import sys

test_files = [
    "tests/test_antixray_config.py",
    "tests/test_casino_data.py",
    "tests/test_panel_ui.py",
    "tests/test_integration.py",
    "tests/test_plazas_and_refresh.py",
    "tests/test_structures_data.py",
    "tests/test_towns_and_villages.py"
]

all_passed = True
for tf in test_files:
    res = subprocess.run([sys.executable, tf], capture_output=True, text=True)
    if res.returncode == 0:
        msg = res.stdout.strip().replace("\n", " | ")
        print(f"[PASS] {tf} -> {msg}")
    else:
        all_passed = False
        print(f"[FAIL] {tf}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")

if all_passed:
    print("\n>>> ALL 7 TEST SUITES PASSED 100% PERFECTLY!")
else:
    print("\n>>> SOME TESTS FAILED!")
    sys.exit(1)
