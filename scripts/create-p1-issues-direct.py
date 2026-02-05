#!/usr/bin/env python3
"""
Script to create P1 GitHub issues using GitHub API directly
This script can use either gh CLI or direct API calls with a token
"""

import json
import os
import sys
import subprocess
from pathlib import Path

REPO = "tim-dickey/trivia-app"
SCRIPT_DIR = Path(__file__).parent
P1_ISSUES_FILE = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts/code-review-issues-p1.json"


def check_gh_auth():
    """Check if gh CLI is authenticated"""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def create_issue_with_gh(issue_data):
    """Create a single GitHub issue using gh CLI"""
    title = issue_data['title']
    body = issue_data['body']
    labels = ','.join(issue_data['labels'])
    
    print(f"Creating: {title}")
    
    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", labels
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        issue_url = result.stdout.strip()
        print(f"✓ Created: {issue_url}")
        issue_num = issue_url.split("/")[-1]
        return issue_num
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {title}")
        print(f"  Error: {e.stderr}")
        return None


def create_issues_via_api(issues, token):
    """Create issues using GitHub API directly"""
    import requests
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    api_url = f"https://api.github.com/repos/{REPO}/issues"
    created = []
    
    for issue in issues:
        print(f"Creating: {issue['title']}")
        
        data = {
            "title": issue['title'],
            "body": issue['body'],
            "labels": issue['labels']
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            issue_data = response.json()
            print(f"✓ Created: {issue_data['html_url']}")
            created.append(issue_data['number'])
        except Exception as e:
            print(f"✗ Failed: {issue['title']}")
            print(f"  Error: {e}")
    
    return created


def create_markdown_file(issues):
    """Create a markdown file with all issue details for manual creation"""
    output_file = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts/P1_ISSUES_TO_CREATE.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# P1 Issues to Create\n\n")
        f.write("Copy and paste each section below to create issues manually at:\n")
        f.write("https://github.com/tim-dickey/trivia-app/issues/new\n\n")
        f.write("---\n\n")
        
        for i, issue in enumerate(issues, 1):
            f.write(f"## Issue {i} of {len(issues)}\n\n")
            f.write(f"**Title:**\n```\n{issue['title']}\n```\n\n")
            f.write(f"**Labels:** {', '.join(issue['labels'])}\n\n")
            f.write(f"**Body:**\n```markdown\n{issue['body']}\n```\n\n")
            f.write("---\n\n")
    
    print(f"\n✓ Created markdown file: {output_file}")
    return output_file


def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Creating P1 GitHub Issues" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"Repository: {REPO}")
    print(f"Source File: {P1_ISSUES_FILE}")
    print()
    
    # Load P1 issues
    if not P1_ISSUES_FILE.exists():
        print(f"❌ Error: P1 issues file not found: {P1_ISSUES_FILE}")
        sys.exit(1)
    
    try:
        with open(P1_ISSUES_FILE, 'r', encoding='utf-8') as f:
            p1_data = json.load(f)
        issues = p1_data['issues']
    except Exception as exc:
        print(f"❌ Error: Failed to load issues: {exc}")
        sys.exit(1)
    
    print(f"✓ Loaded {len(issues)} P1 issues from JSON file")
    print()
    
    # Check authentication methods
    has_gh = check_gh_auth()
    github_token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    
    if has_gh:
        print("✓ GitHub CLI authenticated")
        print()
        print(f"Creating {len(issues)} P1 issues using gh CLI...")
        print()
        
        created = []
        for issue in issues:
            issue_num = create_issue_with_gh(issue)
            if issue_num:
                created.append(issue_num)
        
        print()
        print(f"✓ Successfully created {len(created)}/{len(issues)} issues")
        
    elif github_token:
        print("✓ GitHub token found in environment")
        print()
        print(f"Creating {len(issues)} P1 issues using GitHub API...")
        print()
        
        try:
            import requests
            created = create_issues_via_api(issues, github_token)
            print()
            print(f"✓ Successfully created {len(created)}/{len(issues)} issues")
        except ImportError:
            print("❌ Error: 'requests' library not available")
            print("   Install with: pip install requests")
            sys.exit(1)
    
    else:
        print("⚠️  No authentication method available")
        print()
        print("To create issues, you need to either:")
        print("  1. Authenticate with GitHub CLI: gh auth login")
        print("  2. Set GITHUB_TOKEN environment variable")
        print()
        print("Creating markdown file with issue details...")
        print()
        
        markdown_file = create_markdown_file(issues)
        print()
        print("Next steps:")
        print(f"  1. Review the markdown file: {markdown_file}")
        print("  2. Visit: https://github.com/tim-dickey/trivia-app/issues/new")
        print("  3. Copy each issue's title, labels, and body from the markdown file")
        print()
        print("Or authenticate and run this script again:")
        print("  gh auth login")
        print("  python3 scripts/create-p1-issues-direct.py")


if __name__ == "__main__":
    main()
