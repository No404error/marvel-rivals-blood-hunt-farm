# 打成单文件 auto_farm.exe（templates 等资源全部内嵌）
# 用法:
#   powershell -ExecutionPolicy Bypass -File .\build.ps1
#   powershell -ExecutionPolicy Bypass -File .\build.ps1 -Version 1.0.0

param(
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "==> Installing PyInstaller..."
python -m pip install -q pyinstaller

Write-Host "==> Building single-file exe (templates embedded)..."
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }

# Windows: --add-data "源;目标"
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --name auto_farm `
    --console `
    --uac-admin `
    --manifest app.manifest `
    --add-data "templates;templates" `
    auto_farm.py

$exe = Join-Path "dist" "auto_farm.exe"
if (-not (Test-Path $exe)) {
    throw "Build failed: dist\auto_farm.exe not found"
}

$zipName = "marvel-rivals-blood-hunt-farm-v$Version-win64.zip"
$zipPath = Join-Path "dist" $zipName
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

# 发布包只含一个 exe（外加说明可选）
$stage = Join-Path "dist" "_release_stage"
if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
New-Item -ItemType Directory -Path $stage | Out-Null
Copy-Item $exe $stage
Copy-Item "README.md" $stage -ErrorAction SilentlyContinue
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath
Remove-Item -Recurse -Force $stage

Write-Host ""
Write-Host "Done. Single exe with templates inside:"
Write-Host "  $exe"
Write-Host "  $zipPath"
Write-Host ""
Write-Host "Users run auto_farm.exe (UAC admin required)."
