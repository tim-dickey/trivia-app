param(
    [string]$Repo
)

$ErrorActionPreference = 'Stop'

$repo = if ($env:GITHUB_REPOSITORY) { $env:GITHUB_REPOSITORY } else { 'tim-dickey/trivia-app' }

        # Fallback: derive from git remote URL if available
        if (-not $Repo) {
            $gitCmd = Get-Command git -ErrorAction SilentlyContinue
            if ($null -ne $gitCmd) {
                try {
                    $remoteUrl = git remote get-url origin 2>$null
                    if ($remoteUrl) {
                        # Handle SSH and HTTPS GitHub URLs, extracting owner/repo
                        if ($remoteUrl -match '[:/](?<owner>[^/]+)/(?<name>[^/\.]+)(?:\.git)?$') {
                            $Repo = "$($Matches['owner'])/$($Matches['name'])"
                        }
                    }
                } catch {
                    # Ignore errors and allow final fallback
                }
            }
        }

        # Final fallback: original hardcoded repository
        if (-not $Repo) {
            $Repo = 'tim-dickey/trivia-app'
        }
    }
}

$repo = $Repo
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
