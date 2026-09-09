param(
    [int[]]$Seasons = @(2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026),
    [switch]$IncludeSofaScore
)

$ErrorActionPreference = "Stop"
$seasonArgs = $Seasons | ForEach-Object { $_.ToString() }

if ($IncludeSofaScore) {
    python -m src.data.collect_sofascore --date (Get-Date -Format "yyyy-MM-dd")
    if ($LASTEXITCODE -ne 0) { Write-Warning "SofaScore collection failed; continuing with the primary source." }
}

python -m src.data.collect_data --seasons $seasonArgs
if ($LASTEXITCODE -ne 0) { throw "Data collection failed" }

python -m src.models.train --input data/raw/football_data_matches.csv
if ($LASTEXITCODE -ne 0) { throw "Model training failed" }

Write-Host "Data and model update completed successfully."
