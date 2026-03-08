import os
import subprocess
import time
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_adb(args):
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Try finding adb.exe in the same folder (Installer's way)
    adb_path = os.path.join(current_dir, "adb.exe")
    
    # 2. Fallback: Check if it's in a subfolder or System PATH
    if not os.path.exists(adb_path):
        adb_path = "adb" # Use system global adb
        
    try:
        # Increased timeout to 5 for modern devices like S25 FE
        return subprocess.run([adb_path] + args, capture_output=True, text=True, timeout=5)
    except Exception:
        return None

def get_device_info():
    # Fetch model and android version
    m = run_adb(["shell", "getprop", "ro.product.model"])
    v = run_adb(["shell", "getprop", "ro.build.version.release"])
    model = m.stdout.strip() if m and m.stdout else "Unknown"
    ver = v.stdout.strip() if v and v.stdout else "?"
    return f"{model} (Android {ver})"

def check_root():
    # Check if device has root access
    res = run_adb(["shell", "su", "-c", "id"])
    if res and "uid=0" in res.stdout:
        return True
    return False

def main_loop():
    while True:
        clear()
        console.print("[bold cyan]Azeno42's Android Toolset v0.1-alpha[/bold cyan]\n")
        
        # Continuous connection check
        res = run_adb(["devices"])
        if res and "device\n" in res.stdout:
            info = get_device_info()
            is_root = check_root()
            
            # Status panel with root warning
            status_msg = f"[bold green]Connected:[/bold green] {info}"
            if not is_root:
                status_msg += "\n[bold yellow]Root access not found, some features may be limited![/bold yellow]"
            
            console.print(Panel(status_msg, expand=False))
            
            console.print("\n1) Smart Shell\n2) Power Options\nQ) Exit")
            choice = input("\nSelection > ").lower()
            
            if choice == '1':
                run_adb(["root"])
                subprocess.call([os.path.join("platform-tools", "adb.exe"), "shell"])
            elif choice == '2':
                power_menu(info)
            elif choice == 'q':
                break
        else:
            # Global waiting state
            console.print(Panel("[bold red]No Device![/bold red] Waiting for connection...", expand=False))
            time.sleep(2)

def power_menu(info):
    while True:
        clear()
        console.print(f"[bold yellow]Power Options - {info}[/bold yellow]\n")
        console.print("1) Reboot\n2) Recovery\n3) Download\nB) Back")
        
        # Check connection inside sub-menu
        res = run_adb(["devices"])
        if not (res and "device\n" in res.stdout):
            break

        c = input("\nAction > ").lower()
        if c == '1': run_adb(["reboot"])
        elif c == '2': run_adb(["reboot", "recovery"])
        elif c == '3': run_adb(["reboot", "download"])
        elif c == 'b': break

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        pass