#!/usr/bin/env python3
"""
Script to create GitHub issues from code review findings using GitHub CLI

Supports all 4 priority levels:
  - P0 (critical): System-breaking issues blocking development
  - P1 (high): Important features/fixes needed soon
  - P2 (medium): Improvements and enhancements
  - P3 (low): Nice-to-have improvements and optimizations
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional

REPO = (os.environ.get("GITHUB_REPOSITORY") or "").strip() or "tim-dickey/trivia-app"
SCRIPT_DIR = Path(__file__).parent
ISSUES_DIR = SCRIPT_DIR.parent / "_bmad-output/implementation-artifacts"

# Priority mapping
PRIORITY_LABELS = {
    "critical": ["priority:critical"],
    "high": ["priority:high"],
    "medium": ["priority:medium"],
    "low": ["priority:low"],
}

def check_gh_auth() -> bool:
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

def create_issue(title: str, body: str, labels: List[str]) -> Optional[str]:
    """Create a single GitHub issue
    
    Args:
        title: Issue title
        body: Issue description/body
        labels: List of labels to apply
        
    Returns:
        Issue number if successful, None if failed
    """
    print(f"Creating: {title}")
    
    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", body,
        "--label", ",".join(labels) if labels else ""
    ]
    
    # Remove empty label argument
    cmd = [arg for arg in cmd if arg != ""]
    
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

def load_issues_from_json(filepath: Path) -> List[Dict]:
    """Load issues from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        List of issue dictionaries
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get('issues', [])

def validate_issue(issue: Dict) -> Tuple[bool, Optional[str]]:
    """Validate that issue has all required fields
    
    Args:
        issue: Issue dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['title', 'body', 'labels', 'priority']
    for field in required_fields:
        if field not in issue:
            return False, f"Missing required field: {field}"
        if not issue[field]:
            return False, f"Empty required field: {field}"
    
    # Validate priority level
    if issue['priority'] not in PRIORITY_LABELS:
        valid_priorities = ", ".join(PRIORITY_LABELS.keys())
        return False, f"Invalid priority '{issue['priority']}'. Must be one of: {valid_priorities}"
    
    return True, None

def get_all_issue_files() -> List[Tuple[Path, str]]:
    """Get all issue JSON files for all priority levels
    
    Returns:
        List of (filepath, priority_label) tuples
    """
    issue_files = [
        ("code-review-issues-p0.json", "P0 (Critical)"),
        ("code-review-issues-p1.json", "P1 (High)"),
        ("code-review-issues-p2.json", "P2 (Medium)"),
        ("code-review-issues-p3.json", "P3 (Low)"),
    ]
    
    return [(ISSUES_DIR / filename, label) for filename, label in issue_files]

def main():
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "Creating GitHub Issues from Code Review Findings" + " " * 14 + "║")
    print("║" + " " * 20 + "Supports P0, P1, P2, P3 Priority Levels" + " " * 20 + "║")
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
    priority_counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    
    for filepath, priority_label in get_all_issue_files():
        if filepath.exists():
            issues = load_issues_from_json(filepath)
            all_issues.extend(issues)
            priority_key = priority_label.split()[0]
            priority_counts[priority_key] = len(issues)
            print(f"✓ Loaded {len(issues)} issues from {filepath.name} ({priority_label})")
        else:
            priority_key = priority_label.split()[0]
            print(f"⚠️  {filepath.name} ({priority_label}) not found. Skipping.")
    
    print()
    print(f"Priority Breakdown:")
    for priority in ["P0", "P1", "P2", "P3"]:
        count = priority_counts[priority]
        if count > 0:
            print(f"  {priority}: {count} issues")
    
    total = sum(priority_counts.values())
    print()
    print(f"Total issues to create: {total}")
    print()
    
    if total == 0:
        print("No issues found to create. Exiting.")
        sys.exit(0)
    
    # Create issues
    created_issues = []
    failed_issues = []
    
    for idx, issue in enumerate(all_issues, 1):
        # Validate issue before creating
        is_valid, error_msg = validate_issue(issue)
        if not is_valid:
            print(f"⚠️  [{idx}/{total}] Skipping invalid issue: {error_msg}")
            print(f"   Issue ID: {issue.get('id', 'unknown')}")
            print()
            failed_issues.append({
                'id': issue.get('id', 'unknown'),
                'error': error_msg
            })
            continue
        
        # Build label list with priority label
        labels = issue.get('labels', [])
        priority = issue.get('priority')
        priority_label = PRIORITY_LABELS.get(priority, [])
        all_labels = list(set(labels + priority_label))  # Avoid duplicates
        
        print(f"[{idx}/{total}] ", end="")
        issue_num = create_issue(
            issue['title'],
            issue['body'],
            all_labels
        )
        if issue_num:
            created_issues.append({
                'number': issue_num,
                'title': issue['title'],
                'priority': issue.get('priority', 'unknown'),
                'priority_label': issue.get('id', '').split('-')[0] if issue.get('id') else 'unknown'
            })
        else:
            failed_issues.append({
                'id': issue.get('id', 'unknown'),
                'title': issue['title'],
                'error': 'Failed to create issue'
            })
        
        time.sleep(1)  # Rate limiting
        print()
    
    # Summary
    print("═" * 80)
    print(" Summary")
    print("═" * 80)
    print()
    print(f"Successfully created: {len(created_issues)}/{total} issues")
    if failed_issues:
        print(f"Failed: {len(failed_issues)} issues")
    print()
    
    if created_issues:
        print("Created Issues by Priority:")
        print()
        for priority in ["P0", "P1", "P2", "P3"]:
            priority_issues = [i for i in created_issues if i['priority_label'] == priority]
            if priority_issues:
                priority_name = PRIORITY_LABELS[priority.lower()][0].split(':')[1] if priority.lower() in PRIORITY_LABELS else "unknown"
                print(f"  {priority} ({priority_name}):")
                for issue in priority_issues:
                    print(f"    #{issue['number']} - {issue['title']}")
                print()
        
        # Save tracking file
        tracking_file = ISSUES_DIR / "code-review-issues-tracking.md"
        with open(tracking_file, 'w') as f:
            f.write("# Code Review Issues Tracking\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Source: Code Review 2026-02-02\n\n")
            f.write("## Created Issues\n\n")
            
            for priority in ["P0", "P1", "P2", "P3"]:
                priority_issues = [i for i in created_issues if i['priority_label'] == priority]
                if priority_issues:
                    priority_name = PRIORITY_LABELS[priority.lower()][0].split(':')[1] if priority.lower() in PRIORITY_LABELS else "unknown"
                    f.write(f"### {priority} ({priority_name})\n\n")
                    for issue in priority_issues:
                        f.write(f"- [ ] #{issue['number']} - {issue['title']}\n")
                    f.write("\n")
        
        print(f"✓ Issue tracking saved to: {tracking_file}")
    
    if failed_issues:
        print()
        print("Failed Issues:")
        for issue in failed_issues:
            print(f"  {issue['id']}: {issue.get('error', 'Unknown error')}")
    
    print()
    print("✓ Issue creation complete!")
    return 0 if len(failed_issues) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
