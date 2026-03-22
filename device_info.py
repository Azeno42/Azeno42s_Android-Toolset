import time
from rich.table import Table
from core import *

def show_advanced_info(console):
    table = Table(title="Azeno42 - Device Information", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    # 1. Battery Level (Advanced parsing to fix -1% bug)
    bat_res = run_adb(["shell", "dumpsys", "battery"])
    level = "Unknown"
    if bat_res and bat_res.stdout:
        for line in bat_res.stdout.splitlines():
            if "level" in line.lower():
                # Extracting digits only to avoid formatting issues
                import re
                digits = re.findall(r'\d+', line)
                if digits:
                    level = f"{digits[0]}%"
    
    # 2. Storage Info (Refined for /data)
    storage_res = run_adb(["shell", "df", "-h", "/data"])
    usage = "N/A"
    if storage_res and storage_res.stdout:
        lines = storage_res.stdout.splitlines()
        for line in lines:
            if "/data" in line:
                # Find the percentage value in the line
                parts = line.split()
                for p in parts:
                    if "%" in p:
                        usage = p
                        break

    # 3. Resolution & Identity
    res = "N/A"
    wm_res = run_adb(["shell", "wm", "size"])
    if wm_res and ":" in wm_res.stdout:
        res = wm_res.stdout.split(":")[1].strip()

    full_name = get_device_name()

    # Add rows
    table.add_row("Device Identity", full_name)
    table.add_row("Battery Level", level)
    table.add_row("Storage (/data)", usage)
    table.add_row("Screen Size", res)

    clear()
    console.print(table)
    input(f"\n{L['action']} > Press Enter to return...")