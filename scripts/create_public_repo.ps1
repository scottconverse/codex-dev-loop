param(
    [string]$Repo = "scottconverse/codex-dev-loop"
)

$ErrorActionPreference = "Stop"

gh auth status

$Name = ($Repo -split "/")[1]
gh repo create $Repo --public --source . --remote origin --description "Durable development workflow system for Codex desktop." --push
git tag v0.1.0
git push origin v0.1.0
python scripts\seed_discussions.py --repo $Repo

Write-Host "Published https://github.com/$Repo"
