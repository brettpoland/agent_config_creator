# Build script to create a standalone exe using PyInstaller
# Run from repository root in PowerShell:
# & ./.venv/Scripts/Activate.ps1; & .\build_exe.ps1

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-Not (Test-Path $py)) {
    Write-Error "Python executable not found at $py. Activate your venv or adjust the path."
    exit 1
}

# Clean previous builds
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .\build, .\dist, .\config_app.spec

# Run PyInstaller to build a single-windowed file and embed the icon
$icon = Join-Path $PSScriptRoot "img\app.ico"
if (-Not (Test-Path $icon)) {
    Write-Warning "Icon $icon not found - building without custom icon."
    & $py -m PyInstaller --noconfirm --onefile --windowed "config_app.py"
} else {
    & $py -m PyInstaller --noconfirm --onefile --windowed --icon "$icon" "config_app.py"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build succeeded. Executable at: $(Join-Path $PSScriptRoot 'dist\config_app.exe')"
} else {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
}
