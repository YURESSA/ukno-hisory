[CmdletBinding()]
param(
    [string]$PythonExe = "python"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

function Copy-IfMissing {
    param(
        [string]$SourcePath,
        [string]$TargetPath
    )

    if (-not (Test-Path $TargetPath) -and (Test-Path $SourcePath)) {
        Copy-Item $SourcePath $TargetPath
        Write-Host "Created $TargetPath from template."
    }
}

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    & $PythonExe -m venv $venvPath
}

Write-Host "Installing dependencies..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $projectRoot "requirements.txt")

Copy-IfMissing -SourcePath (Join-Path $projectRoot ".env.example") -TargetPath (Join-Path $projectRoot ".env")

Write-Host "Running migrations..."
Push-Location $projectRoot
try {
    & $venvPython -m alembic upgrade head
}
finally {
    Pop-Location
}

Write-Host "Development setup completed."
