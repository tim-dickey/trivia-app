#!/bin/bash
# Wrapper script for GitHub issue creation using unified script
# This script discovers the repository and calls create_issues.py

set -e

# Discover repository in priority order:
# 1. Environment variable
# 2. Git remote
# 3. Fallback

if [ -n "$GITHUB_REPOSITORY" ]; then
    REPO="$GITHUB_REPOSITORY"
    echo "Using repository from environment: $REPO"
elif command -v git &> /dev/null; then
    # Try to get from git remote
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [ -n "$REMOTE_URL" ]; then
        # Extract owner/repo from SSH or HTTPS URL
        if [[ "$REMOTE_URL" =~ [:/]([^/]+)/([^/\.]+)(\.git)?$ ]]; then
            REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
            echo "Using repository from git remote: $REPO"
        else
            REPO="tim-dickey/trivia-app"
            echo "Using default repository: $REPO"
        fi
    else
        REPO="tim-dickey/trivia-app"
        echo "Using default repository: $REPO"
    fi
else
    REPO="tim-dickey/trivia-app"
    echo "Using default repository: $REPO"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                GitHub Issue Creation - Unified Script                        ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Repository: $REPO"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Export repository for config module
export GITHUB_REPOSITORY="$REPO"

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found. Please install Python 3.7+"
    exit 1
fi

# Run unified script with any additional arguments
$PYTHON_CMD "${SCRIPT_DIR}/create_issues.py" "$@"

EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Script completed successfully"
else
    echo "✗ Script exited with code: $EXIT_CODE"
fi

exit $EXIT_CODE
