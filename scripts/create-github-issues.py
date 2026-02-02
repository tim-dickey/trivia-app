#!/usr/bin/env python3
"""
Script to create GitHub issues from code review findings
Uses subprocess to call gh CLI
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = "tim-dickey/trivia-app"
SCRIPT_DIR = Path(__file__).parent
ISSUES_DIR = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts"

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
        print("❌ Error: gh CLI not found. Please install GitHub CLI.")
        return False

def create_issue(title, body, labels):
    """Create a single GitHub issue"""
    print(f"Creating: {title}")
    
    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", ",".join(labels)
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
        # Extract issue number
        issue_num = issue_url.split("/")[-1]
        return issue_num
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {title}")
        print(f"  Error: {e.stderr}")
        return None

def load_issues_from_json(filepath):
    """Load issues from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get('issues', [])

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "Creating GitHub Issues from Code Review" + " " * 19 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"Repository: {REPO}")
    print()
    
    # Check authentication
    if not check_gh_auth():
        print()
        print("Please authenticate with: gh auth login")
        sys.exit(1)
    
    print("✓ GitHub CLI authenticated")
    print()
    
    # Load all issues
    all_issues = []
    issue_files = [
        "code-review-issues-p0.json",
        "code-review-issues-p1.json",
        "code-review-issues-p2.json"
    ]
    
    for filename in issue_files:
        filepath = ISSUES_DIR / filename
        if filepath.exists():
            issues = load_issues_from_json(filepath)
            all_issues.extend(issues)
            print(f"✓ Loaded {len(issues)} issues from {filename}")
    
    print()
    print(f"Total issues to create: {len(all_issues)}")
    print()
    
    # Create issues
    created_issues = []
    for issue in all_issues:
        issue_num = create_issue(
            issue['title'],
            issue['body'],
            issue['labels']
        )
        if issue_num:
            created_issues.append({
                'number': issue_num,
                'title': issue['title'],
                'priority': issue['priority']
            })
        time.sleep(1)  # Rate limiting
        print()
    
    # Summary
    print("═" * 80)
    print(" Summary")
    print("═" * 80)
    print()
    print(f"Successfully created: {len(created_issues)}/{len(all_issues)} issues")
    print()
    
    if created_issues:
        print("Created Issues:")
        for issue in created_issues:
            print(f"  #{issue['number']} - {issue['title']}")
        
        # Save tracking file
        tracking_file = ISSUES_DIR / "code-review-issues-tracking.md"
        with open(tracking_file, 'w') as f:
            f.write("# Code Review Issues Tracking\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Source: Code Review 2026-02-02\n\n")
            f.write("## Created Issues\n\n")
            for issue in created_issues:
                f.write(f"- [ ] #{issue['number']} - {issue['title']}\n")
        
        print()
        print(f"✓ Issue tracking saved to: {tracking_file}")
    
    print()
    print("✓ Issue creation complete!")

if __name__ == "__main__":
    main()
