#!/usr/bin/env python3
"""
Script to create P1 (High Priority) GitHub issues from code-review-issues-p1.json

This script reads the P1 issues from the JSON file and creates GitHub issues
for each one using the GitHub CLI.

Usage:
    python3 scripts/create-p1-issues.py

Prerequisites:
    - GitHub CLI (gh) installed and authenticated
    - Run: gh auth login
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = "tim-dickey/trivia-app"
SCRIPT_DIR = Path(__file__).parent
P1_ISSUES_FILE = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts/code-review-issues-p1.json"
TRACKING_FILE = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts/p1-issues-created.json"


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
        print("   Visit: https://cli.github.com/")
        return False


def create_issue(issue_data):
    """Create a single GitHub issue from P1 issue data"""
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
        # Extract issue number
        issue_num = issue_url.split("/")[-1]
        return issue_num
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {title}")
        print(f"  Error: {e.stderr}")
        return None


def load_existing_tracking():
    """Load existing tracking data if available"""
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Ensure the data has the expected structure
            if not isinstance(data, dict):
                raise ValueError("Tracking data is not a JSON object")
            if "issues" not in data:
                data["issues"] = []
            if "created_at" not in data:
                data["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            return data
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print(f"⚠️ Warning: Tracking file '{TRACKING_FILE}' is invalid or corrupted: {exc}")
            print("   Proceeding as if no issues have been created yet.")
    return {
        "created_at": time.strftime('%Y-%m-%d %H:%M:%S'),
        "issues": []
    }


def save_tracking(tracking_data):
    """Save tracking data to file"""
    tracking_data["last_updated"] = time.strftime('%Y-%m-%d %H:%M:%S')
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracking_data, f, indent=2)
    print(f"✓ Tracking file updated: {TRACKING_FILE}")


def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "Creating P1 GitHub Issues from JSON File" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"Repository: {REPO}")
    print(f"Source File: {P1_ISSUES_FILE}")
    print()
    
    # Check authentication
    if not check_gh_auth():
        print()
        print("Please authenticate with GitHub CLI first:")
        print("  gh auth login")
        sys.exit(1)
    
    print("✓ GitHub CLI authenticated")
    print()
    
    # Load P1 issues
    if not P1_ISSUES_FILE.exists():
        print(f"❌ Error: P1 issues file not found: {P1_ISSUES_FILE}")
        sys.exit(1)
    
    try:
        with open(P1_ISSUES_FILE, 'r', encoding='utf-8') as f:
            p1_data = json.load(f)
        issues = p1_data['issues']
    except json.JSONDecodeError as exc:
        print(f"❌ Error: Failed to parse JSON from {P1_ISSUES_FILE}: {exc}")
        sys.exit(1)
    except KeyError:
        print(f"❌ Error: JSON file {P1_ISSUES_FILE} is missing required 'issues' key.")
        sys.exit(1)
    print(f"✓ Loaded {len(issues)} P1 issues from JSON file")
    print()
    
    # Load existing tracking
    tracking = load_existing_tracking()
    created_ids = set(item['id'] for item in tracking['issues'])
    
    # Filter out already created issues
    issues_to_create = [i for i in issues if i['id'] not in created_ids]
    already_created = [i for i in issues if i['id'] in created_ids]
    
    if already_created:
        print(f"ℹ️  {len(already_created)} issues already created, skipping:")
        for issue in already_created:
            issue_id = issue['id']
            # Find the tracking info
            tracking_info = next((t for t in tracking['issues'] if t['id'] == issue_id), None)
            if tracking_info:
                print(f"   - {issue_id}: #{tracking_info['github_issue_number']} {issue['title']}")
        print()
    
    if not issues_to_create:
        print("✓ All P1 issues have already been created!")
        sys.exit(0)
    
    print(f"Creating {len(issues_to_create)} new P1 issues...")
    print()
    
    # Create issues
    created_issues = []
    for issue in issues_to_create:
        issue_num = create_issue(issue)
        if issue_num:
            created_issues.append({
                'id': issue['id'],
                'github_issue_number': issue_num,
                'title': issue['title'],
                'priority': issue['priority'],
                'effort_hours': issue['effort_hours'],
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            # Add to tracking
            tracking['issues'].append(created_issues[-1])
        time.sleep(1)  # Rate limiting
        print()
    
    # Save tracking file
    if created_issues:
        save_tracking(tracking)
    
    # Summary
    print()
    print("═" * 80)
    print(" Summary")
    print("═" * 80)
    print()
    print(f"Successfully created: {len(created_issues)}/{len(issues_to_create)} P1 issues")
    print()
    
    if created_issues:
        print("Created Issues:")
        for issue in created_issues:
            print(f"  #{issue['github_issue_number']} - {issue['title']}")
            print(f"      Effort: {issue['effort_hours']} hours")
        
        total_effort = sum(i['effort_hours'] for i in created_issues)
        print()
        print(f"Total Effort: {total_effort} hours ({total_effort/8:.1f} days)")
    
    print()
    print("✓ P1 issue creation complete!")
    print()
    print("Next steps:")
    print("  1. Review created issues at https://github.com/tim-dickey/trivia-app/issues")
    print("  2. Assign issues to team members")
    print("  3. Add to project board if needed")
    print("  4. Start implementation based on priority")


if __name__ == "__main__":
    main()
