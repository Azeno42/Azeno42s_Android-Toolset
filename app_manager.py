from core import *
from rich.console import Console
from rich.table import Table

def show_app_menu(console):
    while True:
        clear()
        # Header using the core language dictionary
        console.print(f"[bold cyan]Azeno42 - App Management[/bold cyan]\n")
        console.print("1) List All Packages\n2) Uninstall Package (Debloat)\nB) Back")
        
        # Connection Check
        res = run_adb(["devices"])
        if not (res and "device\n" in res.stdout):
            break

        choice = input(f"\n{L['action']} > ").lower()

        if choice == '1':
            # Fetch all installed third-party and system packages
            pkgs = run_adb(["shell", "pm", "list", "packages"])
            if pkgs:
                console.print("\n[bold yellow]Installed Packages:[/bold yellow]")
                # We show first 20 to avoid scrolling issues, or use a simple list
                pkg_list = pkgs.stdout.splitlines()[:30] 
                for p in pkg_list:
                    console.print(f"[dim]- {p.replace('package:', '')}[/dim]")
                console.print(f"\n[italic]Showing first 30 packages...[/italic]")
                input("\nPress Enter to continue...")

        elif choice == '2':
            # The actual Debloat logic
            pkg_name = input("\nEnter Package Name (e.g., com.facebook.katana): ").strip()
            if pkg_name:
                # Command: pm uninstall -k --user 0 <package>
                # This uninstalls for the current user without needing full root
                result = run_adb(["shell", "pm", "uninstall", "-k", "--user", "0", pkg_name])
                if "Success" in result.stdout:
                    console.print(f"[bold green]Successfully uninstalled: {pkg_name}[/bold green]")
                else:
                    console.print(f"[bold red]Failed to uninstall: {pkg_name}[/bold red]")
                time.sleep(2)

        elif choice == 'b':
            break