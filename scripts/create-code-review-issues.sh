#!/bin/bash
# Script to create GitHub issues for code review findings
# Generated: 2026-02-02
# Source: Code Review of PR #20

set -e

REPO="tim-dickey/trivia-app"

echo "Creating GitHub issues for code review findings..."
echo "Repository: $REPO"
echo ""

# Check if gh is authenticated
if ! gh auth status &>/dev/null; then
    echo "ERROR: GitHub CLI is not authenticated."
    echo "This script requires GitHub authentication."
    echo ""
    echo "The script will now execute in the current authenticated session."
fi

# Array to store created issue numbers
declare -a ISSUE_NUMBERS=()
SUCCESS_COUNT=0

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    echo "Creating: $title"
    
    issue_url=$(gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "$labels" \
        2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✓ Created: $issue_url"
        issue_num=$(echo "$issue_url" | grep -oP '/issues/\K[0-9]+' || echo "unknown")
        ISSUE_NUMBERS+=("$issue_num|$title")
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo ""
        sleep 1
    else
        echo "✗ Failed: $title"
        echo ""
    fi
}

echo "Creating P0 (Critical) Issues..."
echo "================================"
echo ""
