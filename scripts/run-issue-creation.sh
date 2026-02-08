#!/bin/bash
# Wrapper script that calls gh CLI to create issues
# This script will be executed with proper authentication

set -e

REPO="tim-dickey/trivia-app"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║          Creating GitHub Issues from Code Review Findings                   ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Repository: $REPO"
echo ""

# Note: This script should be run with proper GitHub authentication
# If gh is not authenticated, it will use the current session's credentials

echo "Note: Issue count varies based on BMAD review results"
echo "This may take a few minutes..."
echo ""

# Trigger issue creation using the Python helper script
echo "Please wait while issues are created..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export GITHUB_REPOSITORY="$REPO"
python3 "${SCRIPT_DIR}/create-github-issues.py"
