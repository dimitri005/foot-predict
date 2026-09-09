$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

python -m src.data.refresh_daily --window-days 3 --delay 1
if ($LASTEXITCODE -ne 0) {
    throw "Daily fixture refresh failed"
}

Write-Host "Daily football fixtures refreshed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
