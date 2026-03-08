import os
import subprocess
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_adb(args):
    """Internal function to run ADB commands from the local folder."""
    adb_path = os.path.join("platform-tools", "adb.exe")
    # Using 'subprocess.run' for stable command execution
    return subprocess.run([adb_path] + args, capture_output=True, text=True)

def startup():
    clear()
    console.print("[bold cyan]Azeno42's Android Toolset v0.1[/bold cyan] [white]| Azeno42_Tech[/white]")
    console.print("[white]------------------------------------------------[/white]\n")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        # Check ADB Engine
        progress.add_task(description="Linking ADB Engine...", total=None)
        time.sleep(1)
        
        # Check Device
        task2 = progress.add_task(description="Searching for devices...", total=None)
        res = run_adb(["devices"])
        
    if "device\n" in res.stdout:
        console.print("[bold green]{ADB Engine...} [OK][/bold green]")
        console.print("[bold green]{Device Status...} [CONNECTED][/bold green]")
        return True
    else:
        console.print("[bold red]{Device Status...} [NOT FOUND][/bold red]")
        console.print("[yellow]Please connect your S20 FE / S25 FE and enable USB Debugging.[/yellow]")
        return False

def smart_shell():
    """The 'Uçuk' feature: Auto-detect root and enter shell."""
    console.print("\n[bold blue]Checking Root Access...[/bold blue]")
    # Try to run 'adb root' (Common in LineageOS)
    run_adb(["root"])
    time.sleep(1)
    
    # Enter the actual shell
    adb_path = os.path.join("platform-tools", "adb.exe")
    subprocess.call([adb_path, "shell"])

def main():
    if startup():
        console.print("\n1) Enter Smart Shell (Root/User)")
        console.print("2) Power Options (Reboot Menu)")
        console.print("Q) Exit")
        
        choice = input("\nSelection > ")
        if choice == '1':
            smart_shell()
        elif choice.lower() == 'q':
            exit()

if __name__ == "__main__":
    main()