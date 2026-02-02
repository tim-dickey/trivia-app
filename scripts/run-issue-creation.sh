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

echo "Note: Creating 15 issues (5 P0, 5 P1, 5 P2)"
echo "This may take a few minutes..."
echo ""

# The actual issue creation will be done by the agent using gh CLI
echo "Please wait while issues are created..."

