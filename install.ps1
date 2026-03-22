# Azeno42 Android Toolset - System Deployment Script (v0.3-beta)
# Requires Administrator privileges

if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[!] Error: Please run as Administrator!" -ForegroundColor Red
    pause; exit
}

# --- 1. Language Selection ---
Write-Host "Select Installation Language / Dil Secin:" -ForegroundColor Cyan
Write-Host "1) English (Default)"
Write-Host "2) Turkce"
$langChoice = Read-Host "Choice (1/2)"
$lang = if ($langChoice -eq "2") { "tr" } else { "en" }

$installDir = "$env:ProgramFiles\Azeno42-Toolset"
$baseUrl = "https://raw.githubusercontent.com/Azeno42/Azeno42s_Android-Toolset/main"
$modules = @("main.py", "core.py", "device_info.py", "app_manager.py", "settings.py")

# --- 2. Environment Setup ---
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "[*] Directory created: $installDir" -ForegroundColor White
}

# --- 3. ADB Deployment ---
Write-Host "[*] Downloading Android Platform-Tools..." -ForegroundColor Yellow
$ptUrl = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
$ptZip = "$installDir\pt.zip"
Invoke-WebRequest -Uri $ptUrl -OutFile $ptZip
Expand-Archive -Path $ptZip -DestinationPath $installDir -Force
Remove-Item $ptZip
Move-Item -Path "$installDir\platform-tools\*" -Destination $installDir -Force
Remove-Item "$installDir\platform-tools" -Recurse

# --- 4. Module Deployment & Patching ---
foreach ($file in $modules) {
    Write-Host "[*] Fetching $file from GitHub..." -ForegroundColor Yellow
    $targetFile = "$installDir\$file"
    Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile $targetFile
    
    # Patch the language setting directly into core.py during install
    if ($file -eq "core.py") {
        (Get-Content $targetFile) -replace 'current_lang = ".*"', "current_lang = `"$lang`"" | Set-Content $targetFile
    }
}

# --- 5. Python & Dependency Check ---
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Python not found. Installing via Winget..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --silent
}
Write-Host "[*] Installing 'rich' UI library..." -ForegroundColor Cyan
python -m pip install rich --quiet

# --- 6. PATH & CLI Configuration ---
$oldPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($oldPath -notlike "*$installDir*") {
    Write-Host "[*] Adding Toolset to System PATH..." -ForegroundColor Cyan
    [Environment]::SetEnvironmentVariable("Path", $oldPath + ";$installDir", "Machine")
}

# Create executable batch file
$batchFile = "$installDir\azeno.bat"
"@echo off`npython ""$installDir\main.py"" %*" | Out-File -FilePath $batchFile -Encoding ASCII

Write-Host "`n[SUCCESS] Azeno42 Toolset v0.3-beta is now installed!" -ForegroundColor Green
Write-Host "[*] You can now type 'azeno' in any terminal to start." -ForegroundColor White
pause