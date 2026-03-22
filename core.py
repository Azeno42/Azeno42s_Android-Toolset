import os
import subprocess

def clear():
    # Clears the terminal screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')

def get_adb_path():
    # Returns local adb path or system global adb
    current_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(current_dir, "adb.exe")
    return adb_path if os.path.exists(adb_path) else "adb"

def run_adb(args):
    # Executes ADB commands with a 5s timeout
    try:
        return subprocess.run([get_adb_path()] + args, capture_output=True, text=True, timeout=5)
    except Exception:
        return None

def check_root():
    # Execute root check
    result = run_adb(["shell", "su", "-c", "id"])
    if result and "uid=0" in result.stdout:
        return True
    return False

def get_device_name():
    # Gets brand and model like 'samsung SM-S731B'
    brand = run_adb(["shell", "getprop", "ro.product.brand"])
    model = run_adb(["shell", "getprop", "ro.product.model"])
    
    b_text = brand.stdout.strip() if brand and brand.stdout else ""
    m_text = model.stdout.strip() if model and model.stdout else "Device"
    
    return f"{b_text} {m_text}".strip()

# Global language dictionary
LANGS = {
    "tr": {
        "title": "Azeno42 Android Toolset v0.3-beta",
        "no_device": "[bold red]Cihaz Yok![/bold red] Baglanti bekleniyor...",
        "connected": "[bold green]Bagli:[/bold green]",
        "root_fail": "[bold yellow]Root bulunamadi, bazi ozellikler kisitli![/bold yellow]",
        "main_menu": "1) Akilli Kabuk\n2) Guc Secenekleri\n3) Cihaz Bilgisi\n4) Uygulama Yonetimi\nS) Ayarlar\nQ) Cikis",
        "power_menu_title": "Guc Secenekleri",
        "power_options": "1) Yeniden Baslat\n2) Recovery\n3) Download\nB) Geri",
        "selection": "Secim",
        "action": "Islem"
    },
    "en": {
        "title": "Azeno42's Android Toolset v0.3-beta",
        "no_device": "[bold red]No Device![/bold red] Waiting for connection...",
        "connected": "[bold green]Connected:[/bold green]",
        "root_fail": "[bold yellow]Root access not found, some features may be limited![/bold yellow]",
        "main_menu": "1) Smart Shell\n2) Power Options\n3) Device Info\n4) App Management\nS) Settings\nQ) Exit",
        "power_menu_title": "Power Options",
        "power_options": "1) Reboot\n2) Recovery\n3) Download\nB) Back",
        "selection": "Selection",
        "action": "Action"
    }
}

current_lang = "en"
L = LANGS[current_lang]