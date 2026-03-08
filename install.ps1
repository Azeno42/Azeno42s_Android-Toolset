# Azeno42 Android Toolset - System Deployment Script
# Admin check
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "[!] Lutfen bu dosyayi Yonetici olarak calistirin!" -ForegroundColor Red
    pause
    exit
}

$installDir = "$env:ProgramFiles\Azeno42-Toolset"
Write-Host "--- Azeno42 Toolset System Setup ---" -ForegroundColor Cyan

# 1. Create Directory
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "[*] Directory created: $installDir" -ForegroundColor White
}

# 2. Download Platform Tools from Google
Write-Host "[*] Downloading Platform-Tools..." -ForegroundColor Yellow
$ptUrl = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
$ptZip = "$installDir\pt.zip"
Invoke-WebRequest -Uri $ptUrl -OutFile $ptZip
Expand-Archive -Path $ptZip -DestinationPath $installDir -Force
Remove-Item $ptZip
# Move files out of the 'platform-tools' subfolder to match your main.py logic
Move-Item -Path "$installDir\platform-tools\*" -Destination $installDir -Force
Remove-Item "$installDir\platform-tools" -Recurse

# 3. Download main.py from GitHub
Write-Host "[*] Fetching main.py from GitHub..." -ForegroundColor Yellow
$mainUrl = "https://raw.githubusercontent.com/Azeno42/Azeno42s_Android-Toolset/main/main.py"
Invoke-WebRequest -Uri $mainUrl -OutFile "$installDir\main.py"

# 4. Python & Rich Library Check
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Python not found. Installing..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --silent
}
Write-Host "[*] Installing 'rich' library..." -ForegroundColor Cyan
python -m pip install rich --quiet

# 5. Add to System PATH
Write-Host "[*] Adding to System PATH..." -ForegroundColor Cyan
$oldPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($oldPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", $oldPath + ";$installDir", "Machine")
}

Write-Host "`n[SUCCESS] Azeno42 Toolset v0.1-alpha is now installed!" -ForegroundColor Green
Write-Host "You can now type 'python main.py' in any terminal." -ForegroundColor White
pause