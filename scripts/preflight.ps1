[CmdletBinding()]
param(
    [string]$PythonPath = "",
    [string]$NodePath = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

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

$Python = Resolve-Tool @(
    $PythonPath,
    (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"),
    "python",
    "py"
)

$Node = Resolve-Tool @(
    $NodePath,
    (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"),
    "node"
)

Write-Host "StudyOps preflight"
Write-Host "Python: $Python"
Write-Host "Node: $Node"

& $Python -m py_compile `
    app\workflows\studyops_workflow.py `
    app\tools\studyops_tools.py `
    app\fast_api_app.py

& $Node --check frontend\app.js

& $Python -m unittest discover -s tests\unit

Write-Host "StudyOps preflight passed."

