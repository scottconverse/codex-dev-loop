param(
    [string]$Destination = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Source = Join-Path $RepoRoot "skill"

if (-not (Test-Path $Source)) {
    throw "Could not find skill source at $Source"
}

if ([string]::IsNullOrWhiteSpace($Destination)) {
    $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
    $Destination = Join-Path $CodexHome "skills\codex-dev-loop"
}

if ((Test-Path $Destination) -and -not $Force) {
    Write-Host "Destination already exists: $Destination"
    Write-Host "Use -Force to replace it."
    exit 1
}

if (Test-Path $Destination) {
    Remove-Item -Recurse -Force -LiteralPath $Destination
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
Copy-Item -Recurse -Force -LiteralPath $Source -Destination $Destination

Write-Host "Installed codex-dev-loop skill to:"
Write-Host $Destination
Write-Host ""
Write-Host "In Codex desktop, start a new thread or reload context, then say:"
Write-Host "Use `$codex-dev-loop for this repo."
