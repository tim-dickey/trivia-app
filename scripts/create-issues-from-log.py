#!/usr/bin/env python3
"""
Script to create GitHub issues from the consolidated issues log
Uses the issues-log.json file which includes all issues from multiple sources
"""

import json
import subprocess
import sys
import time
from pathlib import Path

REPO = "tim-dickey/trivia-app"
SCRIPT_DIR = Path(__file__).parent
ISSUES_LOG_FILE = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts/issues-log.json"

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

def create_issue(issue_data):
    """Create a single GitHub issue from issue log data"""
    title = issue_data['title']
    print(f"Creating: {title}")
    
    # Build body from issue data
    body_parts = [
        f"**Issue ID**: {issue_data['issue_id']}",
        f"**Source**: {issue_data['source']}",
        f"**Category**: {issue_data['category']}",
        f"**Effort**: {issue_data['effort_hours']} hours",
        "",
        "## Description",
        "",
        issue_data['description'],
        ""
    ]
    
    if issue_data.get('blocks'):
        body_parts.extend([
            "## Blocks",
            "",
            ', '.join(issue_data['blocks']),
            ""
        ])
    
    body_parts.extend([
        "## Acceptance Criteria",
        ""
    ])
    for criterion in issue_data['acceptance_criteria']:
        body_parts.append(f"- [ ] {criterion}")
    
    body_parts.extend([
        "",
        "---",
        f"**Date Identified**: {issue_data['date_identified']}",
        f"**Priority**: {issue_data['priority']}"
    ])
    
    body = '\n'.join(body_parts)
    
    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", ",".join(issue_data['labels'])
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

def update_issues_log(issue_id, github_issue_number):
    """Update the issues log with the created GitHub issue number"""
    with open(ISSUES_LOG_FILE, 'r') as f:
        data = json.load(f)
    
    # Find and update the issue
    for issue in data['issues']:
        if issue['issue_id'] == issue_id:
            issue['github_issue_number'] = int(github_issue_number)
            issue['status'] = 'open'
            issue['date_opened'] = time.strftime('%Y-%m-%d')
            break
    
    # Update summary
    data['summary']['github_issues_created'] = sum(
        1 for i in data['issues'] if i.get('github_issue_number')
    )
    data['summary']['issues_opened'] = sum(
        1 for i in data['issues'] if i.get('status') == 'open'
    )
    data['metadata']['last_updated'] = time.strftime('%Y-%m-%d')
    
    # Save updated data
    with open(ISSUES_LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "Creating GitHub Issues from Consolidated Issues Log" + " " * 11 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"Repository: {REPO}")
    print(f"Issues Log: {ISSUES_LOG_FILE}")
    print()
    
    # Check authentication
    if not check_gh_auth():
        print()
        print("Please authenticate with: gh auth login")
        sys.exit(1)
    
    print("✓ GitHub CLI authenticated")
    print()
    
    # Load issues log
    if not ISSUES_LOG_FILE.exists():
        print(f"❌ Error: Issues log file not found: {ISSUES_LOG_FILE}")
        sys.exit(1)
    
    with open(ISSUES_LOG_FILE, 'r') as f:
        data = json.load(f)
    
    issues = data['issues']
    print(f"✓ Loaded {len(issues)} issues from consolidated log")
    print()
    
    # Show summary
    print("Summary:")
    print(f"  - Total: {data['metadata']['total_issues']} issues")
    print(f"  - P0 (Critical): {data['summary']['by_priority']['critical']} issues")
    print(f"  - P1 (High): {data['summary']['by_priority']['high']} issues")
    print(f"  - P2 (Medium): {data['summary']['by_priority']['medium']} issues")
    print(f"  - Total Effort: {data['summary']['total_effort_days']} days")
    print()
    
    # Filter out already created issues
    issues_to_create = [i for i in issues if not i.get('github_issue_number')]
    already_created = [i for i in issues if i.get('github_issue_number')]
    
    if already_created:
        print(f"ℹ️  {len(already_created)} issues already created, skipping:")
        for issue in already_created:
            print(f"   - {issue['issue_id']}: #{issue['github_issue_number']} {issue['title']}")
        print()
    
    if not issues_to_create:
        print("✓ All issues have already been created!")
        sys.exit(0)
    
    print(f"Creating {len(issues_to_create)} new issues...")
    print()
    
    # Create issues
    created_issues = []
    for issue in issues_to_create:
        issue_num = create_issue(issue)
        if issue_num:
            created_issues.append({
                'id': issue['issue_id'],
                'number': issue_num,
                'title': issue['title'],
                'priority': issue['priority']
            })
            # Update the log file
            update_issues_log(issue['issue_id'], issue_num)
        time.sleep(1)  # Rate limiting
        print()
    
    # Summary
    print("═" * 80)
    print(" Summary")
    print("═" * 80)
    print()
    print(f"Successfully created: {len(created_issues)}/{len(issues_to_create)} issues")
    print()
    
    if created_issues:
        print("Created Issues:")
        for issue in created_issues:
            print(f"  #{issue['number']} - [{issue['priority'].upper()}] {issue['title']}")
        
        print()
        print(f"✓ Issues log updated: {ISSUES_LOG_FILE}")
    
    print()
    print("✓ Issue creation complete!")
    print()
    print("Next steps:")
    print("  1. Review created issues at https://github.com/tim-dickey/trivia-app/issues")
    print("  2. Assign issues to team members")
    print("  3. Add to project board if needed")
    print("  4. Start with P0 (Critical) issues")

if __name__ == "__main__":
    main()
