# Azeno42's Android Toolset (v0.1-alpha) 🚀

A lightweight, terminal-based Android management utility built with Python and ADB. This tool is designed for Android enthusiasts who want a fast, "all-in-one" solution for shell access and device power management.



## ✨ Features
- **Smart Shell:** Automatically detects the device and attempts to gain root (su) access. Fallbacks to standard user shell if root is not available.
- **Dynamic Device Detection:** Real-time identification of connected device models and Android versions.
- **Power Options:** Quick commands to reboot into Recovery, Download Mode (Samsung), or Bootloader/Fastboot.
- **Global Deployment:** Can be installed directly to `Program Files` and accessed from any terminal via System PATH.

## 🛠️ Installation
The easiest way to install the toolset is using the **Azeno_Installer.exe**:

1. Download the latest `Azeno_Installer.exe` from the [Releases](link_to_releases) section.
2. Run the installer as **Administrator**.
3. The installer will automatically:
   - Create a directory in `Program Files`.
   - Download the latest **Android Platform-Tools** from Google.
   - Fetch the core logic from this repository.
   - Configure **Python** and required libraries (`rich`).
   - Add the tool to your **System PATH**.

## 🚀 How to Use
Once installed, simply open any terminal (CMD or PowerShell) and type:
```bash
python main.py
