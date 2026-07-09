<#
 Simple packaging script for Windows using PyInstaller.
 Requirements: installed Python in virtualenv with required packages and PyInstaller.
 Usage: run from project root inside the virtualenv: .\pack\package-windows.ps1
#>

param()

Set-Location $PSScriptRoot\..\
Write-Host "Building React frontend..."
cd frontend
npm run build
cd ..

Write-Host "Creating dist folder and copying build..."
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path dist\frontend -Force | Out-Null
Copy-Item frontend\build\* dist\frontend -Recurse -Force

Write-Host "Running PyInstaller..."
pip install pyinstaller
pyinstaller --onefile --add-data "dist/frontend;frontend" run_app.py

Write-Host "Build complete. Executable in dist\dist\run_app.exe"
