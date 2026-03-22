import os
import time
import subprocess
from rich.console import Console
from rich.panel import Panel

# --- MODULE IMPORTS ---
from core import *
from device_info import show_advanced_info
from app_manager import show_app_menu
from settings import show_settings_menu

console = Console()

def main_loop():
    while True:
        clear()
        console.print(f"[bold cyan]{L['title']}[/bold cyan]\n")
        
        # Check for device connection
        res = run_adb(["devices"])
        
        if res and "device\n" in res.stdout:
            # Get device identity and root status
            device_name = get_device_name() # From core.py
            is_root = check_root()
            
            # Status Message
            status_msg = f"{L['connected']} {device_name}" # Now shows Brand + Model
            if not is_root:
                status_msg += f"\n{L['root_fail']}"
            
            console.print(Panel(status_msg, expand=False))
            console.print(f"\n{L['main_menu']}")
            
            choice = input(f"\n{L['selection']} > ").lower()
            
            # --- MENU LOGIC ---
            if choice == '1':
                adb_cmd = get_adb_path()
                subprocess.call([adb_cmd, "shell"])
                
            elif choice == '2':
                # Power menu placeholder
                console.print("[yellow]Power menu is under maintenance...[/yellow]")
                time.sleep(1)
                
            elif choice == '3':
                show_advanced_info(console)
                
            elif choice == '4':
                show_app_menu(console)

            elif choice == 's':
                show_settings_menu(console)
                
            elif choice == 'q':
                break
        else:
            # No device connected state
            console.print(Panel(L['no_device'], expand=False))
            time.sleep(2)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        pass