$ErrorActionPreference = 'Stop'

$repo = if ($env:GITHUB_REPOSITORY) { $env:GITHUB_REPOSITORY } else { 'tim-dickey/trivia-app' }

Write-Host '============================================================'
Write-Host 'Creating GitHub Issues from Code Review Findings'
Write-Host '============================================================'
Write-Host ''
Write-Host "Repository: $repo"
Write-Host ''
Write-Host 'Note: Issue count varies based on BMAD review results'
Write-Host 'This may take a few minutes...'
Write-Host ''
Write-Host 'Please wait while issues are created...'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:GITHUB_REPOSITORY = $repo

$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $pythonCmd) {
    & py -3 "$scriptDir\create-github-issues.py"
} else {
    & python "$scriptDir\create-github-issues.py"
}
