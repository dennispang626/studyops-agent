[CmdletBinding()]
param(
    [int]$Port = 8000,
    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

function Import-DotEnv {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    Get-Content -LiteralPath $Path | ForEach-Object {
        $Line = $_.Trim()
        if ([string]::IsNullOrWhiteSpace($Line) -or $Line.StartsWith("#")) {
            return
        }

        $Parts = $Line.Split("=", 2)
        if ($Parts.Count -ne 2) {
            return
        }

        $Name = $Parts[0].Trim()
        $Value = $Parts[1].Trim().Trim('"').Trim("'")
        if (-not [string]::IsNullOrWhiteSpace($Name)) {
            [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
        }
    }
}

function Resolve-Tool {
    param([string[]]$Candidates)

    foreach ($Candidate in $Candidates) {
        if ([string]::IsNullOrWhiteSpace($Candidate)) {
            continue
        }

        if (Test-Path -LiteralPath $Candidate) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }

        $Command = Get-Command $Candidate -ErrorAction SilentlyContinue
        if ($Command) {
            return $Command.Source
        }
    }

    throw "Unable to resolve required tool from candidates: $($Candidates -join ', ')"
}

Import-DotEnv ".env"
Import-DotEnv ".env.local"

if (-not $env:ALLOW_ORIGINS) {
    $env:ALLOW_ORIGINS = "https://studyops-agent.vercel.app,http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000,null"
}

if (-not $env:STUDYOPS_OTEL_TO_CLOUD) {
    $env:STUDYOPS_OTEL_TO_CLOUD = "False"
}

$Python = Resolve-Tool @(
    $PythonPath,
    (Join-Path $ProjectRoot ".venv\Scripts\python.exe"),
    (Join-Path $ProjectRoot "..\.venv\Scripts\python.exe"),
    (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"),
    "python",
    "py"
)

Write-Host "StudyOps local backend bridge"
Write-Host "API: http://127.0.0.1:$Port"
Write-Host "Frontend origin allowed: https://studyops-agent.vercel.app"
Write-Host "GOOGLE_API_KEY configured: $([bool]$env:GOOGLE_API_KEY)"
Write-Host "Vault: $($env:STUDYOPS_OBSIDIAN_VAULT)"
Write-Host ""

& $Python -m uvicorn app.fast_api_app:app --host 127.0.0.1 --port $Port
