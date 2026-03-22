import time
from core import *

def show_settings_menu(console):
    # We use global to modify the language in the current session
    global L
    
    while True:
        clear()
        console.print(f"[bold cyan]{L['title']} - Settings[/bold cyan]\n")
        console.print("1) Change Language (TR/EN)\nB) Back")
        
        choice = input(f"\n{L['selection']} > ").lower()
        
        if choice == '1':
            # This logic will be improved in v0.4 with a config.json
            console.print("[yellow]Language toggle requested. Re-run installer for permanent change or wait for v0.4![/yellow]")
            time.sleep(2)
        elif choice == 'b':
            break