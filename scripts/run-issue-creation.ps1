param(
    [string]$Repository = ""
)

$ErrorActionPreference = 'Stop'

# Discover repository in priority order:
# 1. Parameter
# 2. Environment variable
# 3. Git remote
# 4. Fallback

$repo = ""

if ($Repository) {
    $repo = $Repository
    Write-Host "Using repository from parameter: $repo"
} elseif ($env:GITHUB_REPOSITORY) {
    $repo = $env:GITHUB_REPOSITORY
    Write-Host "Using repository from environment: $repo"
} else {
    # Try to get from git remote
    $gitCmd = Get-Command git -ErrorAction SilentlyContinue
    if ($null -ne $gitCmd) {
        try {
            $remoteUrl = git remote get-url origin 2>$null
            if ($remoteUrl) {
                # Handle both SSH (git@github.com:owner/repo.git) and HTTPS (https://github.com/owner/repo.git)
                if ($remoteUrl -match '[:/](?<owner>[^/]+)/(?<name>[^/\.]+)(?:\.git)?$') {
                    $repo = "$($Matches['owner'])/$($Matches['name'])"
                    Write-Host "Using repository from git remote: $repo"
                }
            }
        } catch {
            # Ignore errors, will use fallback
        }
    }
    
    # Final fallback
    if (-not $repo) {
        $repo = 'tim-dickey/trivia-app'
        Write-Host "Using default repository: $repo"
    }
}

Write-Host ''
Write-Host '============================================================'
Write-Host '   GitHub Issue Creation - Unified Script'
Write-Host '============================================================'
Write-Host ''
Write-Host "Repository: $repo"
Write-Host ''

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:GITHUB_REPOSITORY = $repo

# Use new unified script
$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $pythonCmd) {
    & py -3 "$scriptDir\create_issues.py" @args
} else {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $pythonCmd) {
        & python "$scriptDir\create_issues.py" @args
    } else {
        Write-Error "Python not found. Please install Python 3.7+ from https://www.python.org/"
        exit 1
    }
}

$exitCode = $LASTEXITCODE
Write-Host ''
if ($exitCode -eq 0) {
    Write-Host '✓ Script completed successfully'
} else {
    Write-Host "✗ Script exited with code: $exitCode"
}

exit $exitCode
