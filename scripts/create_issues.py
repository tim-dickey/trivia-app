#!/usr/bin/env python3
"""
Unified GitHub Issue Creation Script

This script replaces all previous issue creation scripts:
- create-github-issues.py
- create-issues-from-log.py
- create-p1-issues.py
- create-p1-issues-direct.py
- create-p1-issues.sh
- create-code-review-issues.sh

Features:
- Load from multiple sources (JSON files, consolidated log)
- Filter by priority
- Dry-run mode
- Unified tracking
- Idempotent (skip already created issues)
- Retry logic
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import Config
from lib.github_client import GitHubClient
from lib.issue_validator import validate_issue, normalize_priority, merge_labels
from lib.issue_tracker import IssueTracker


def print_header(title: str) -> None:
    """Print formatted header"""
    print("╔" + "═" * 78 + "╗")
    print("║" + title.center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()


def load_issues_from_json(config: Config, priority_filter: Optional[str] = None) -> List[Dict]:
    """
    Load issues from JSON files (P0/P1/P2/P3)
    
    Args:
        config: Configuration object
        priority_filter: Optional priority to filter (e.g., "p1", "high")
        
    Returns:
        List of issue dictionaries
    """
    priorities = ["p0", "p1", "p2", "p3"]
    
    # If priority filter specified, only load that priority
    if priority_filter:
        normalized = normalize_priority(priority_filter)
        priority_map = {"critical": "p0", "high": "p1", "medium": "p2", "low": "p3"}
        if normalized in priority_map:
            priorities = [priority_map[normalized]]
        elif priority_filter.lower() in priorities:
            priorities = [priority_filter.lower()]
    
    all_issues = []
    
    for priority in priorities:
        filepath = config.get_issue_file(priority)
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                issues = data.get('issues', [])
                all_issues.extend(issues)
                print(f"✓ Loaded {len(issues)} issues from {filepath.name}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Warning: Could not load {filepath.name}: {e}")
        else:
            print(f"⚠️  {filepath.name} not found, skipping")
    
    return all_issues


def load_issues_from_log(config: Config) -> List[Dict]:
    """
    Load issues from consolidated log file
    
    Args:
        config: Configuration object
        
    Returns:
        List of issue dictionaries
    """
    log_file = config.get_issues_log_file()
    
    if not log_file.exists():
        print(f"❌ Error: Issues log file not found: {log_file}")
        return []
    
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
        
        issues = data.get('issues', [])
        print(f"✓ Loaded {len(issues)} issues from {log_file.name}")
        
        # Convert log format to standard issue format
        standardized = []
        for issue in issues:
            standardized.append({
                'id': issue.get('issue_id'),
                'title': issue.get('title'),
                'body': issue.get('description') or issue.get('body', ''),
                'labels': issue.get('labels', []),
                'priority': issue.get('priority', 'medium')
            })
        
        return standardized
    except (json.JSONDecodeError, IOError) as e:
        print(f"❌ Error: Could not load issues log: {e}")
        return []


def filter_issues_by_priority(issues: List[Dict], priority: str) -> List[Dict]:
    """
    Filter issues by priority level
    
    Args:
        issues: List of issue dictionaries
        priority: Priority to filter by
        
    Returns:
        Filtered list of issues
    """
    normalized = normalize_priority(priority)
    return [i for i in issues if normalize_priority(i.get('priority', '')) == normalized]


def create_issues(
    client: GitHubClient,
    tracker: IssueTracker,
    issues: List[Dict],
    dry_run: bool = False,
    rate_limit_delay: float = 1.0
) -> tuple[List[Dict], List[Dict]]:
    """
    Create GitHub issues
    
    Args:
        client: GitHub client
        tracker: Issue tracker
        issues: List of issues to create
        dry_run: If True, only show what would be created
        rate_limit_delay: Delay between issue creations (seconds)
        
    Returns:
        Tuple of (created_issues, failed_issues)
    """
    created = []
    failed = []
    
    total = len(issues)
    
    for idx, issue in enumerate(issues, 1):
        # Validate issue
        is_valid, error_msg = validate_issue(issue)
        if not is_valid:
            print(f"⚠️  [{idx}/{total}] Skipping invalid issue: {error_msg}")
            print(f"   Issue ID: {issue.get('id', 'unknown')}")
            print()
            failed.append({
                'id': issue.get('id', 'unknown'),
                'title': issue.get('title', 'unknown'),
                'error': error_msg
            })
            continue
        
        issue_id = issue.get('id', f"ISSUE-{idx}")
        
        # Check if already created
        if tracker.is_created(issue_id):
            github_num = tracker.get_github_number(issue_id)
            print(f"⏭️  [{idx}/{total}] Already created: {issue['title']}")
            print(f"   Issue #{github_num}")
            print()
            continue
        
        # Merge labels with priority labels
        all_labels = merge_labels(issue.get('labels', []), issue.get('priority', 'medium'))
        
        if dry_run:
            print(f"[DRY RUN] [{idx}/{total}] Would create: {issue['title']}")
            print(f"   Priority: {issue.get('priority')}")
            print(f"   Labels: {', '.join(all_labels)}")
            print()
            continue
        
        # Create issue
        print(f"[{idx}/{total}] ", end="")
        issue_num = client.create_issue(
            issue['title'],
            issue['body'],
            all_labels
        )
        
        if issue_num:
            created.append({
                'id': issue_id,
                'number': issue_num,
                'title': issue['title'],
                'priority': issue.get('priority', 'unknown')
            })
            
            # Track creation
            tracker.mark_created(
                issue_id,
                int(issue_num),
                issue.get('priority', 'unknown'),
                'create_issues.py'
            )
        else:
            failed.append({
                'id': issue_id,
                'title': issue['title'],
                'error': 'Failed to create issue'
            })
        
        # Rate limiting
        if idx < total:
            time.sleep(rate_limit_delay)
        
        print()
    
    return created, failed


def print_summary(created: List[Dict], failed: List[Dict], total: int, dry_run: bool = False) -> None:
    """
    Print summary of issue creation
    
    Args:
        created: List of created issues
        failed: List of failed issues
        total: Total number of issues processed
        dry_run: Whether this was a dry run
    """
    print("═" * 80)
    print(" Summary")
    print("═" * 80)
    print()
    
    if dry_run:
        print(f"[DRY RUN] Would create: {total} issues")
        print()
        return
    
    print(f"Successfully created: {len(created)}/{total} issues")
    if failed:
        print(f"Failed: {len(failed)} issues")
    print()
    
    if created:
        print("Created Issues by Priority:")
        print()
        
        # Group by priority
        by_priority: Dict[str, List[Dict]] = {}
        for issue in created:
            priority = normalize_priority(issue.get('priority', 'unknown'))
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(issue)
        
        # Print in priority order
        for priority in ['critical', 'high', 'medium', 'low']:
            if priority in by_priority:
                issues = by_priority[priority]
                print(f"  {priority.upper()} ({len(issues)} issues):")
                for issue in issues:
                    print(f"    #{issue['number']} - {issue['title']}")
                print()
    
    if failed:
        print("Failed Issues:")
        for issue in failed:
            print(f"  {issue['id']}: {issue.get('error', 'Unknown error')}")
        print()


def main() -> int:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create GitHub issues from code review findings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create all issues from JSON files
  python create_issues.py --source json

  # Create issues from consolidated log
  python create_issues.py --source log

  # Create only P1 (high priority) issues
  python create_issues.py --filter-priority high

  # Dry run (show what would be created)
  python create_issues.py --dry-run

  # Create P0 issues only
  python create_issues.py --source json --filter-priority critical
        """
    )
    
    parser.add_argument(
        '--source',
        choices=['json', 'log'],
        default='json',
        help='Source of issues: json (P0/P1/P2/P3 files) or log (consolidated log)'
    )
    
    parser.add_argument(
        '--filter-priority',
        choices=['critical', 'high', 'medium', 'low', 'p0', 'p1', 'p2', 'p3'],
        help='Only create issues of this priority'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without actually creating issues'
    )
    
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=1.0,
        help='Delay between issue creations in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header("Unified GitHub Issue Creation")
    
    # Initialize configuration
    config = Config()
    print(f"Repository: {config.repo}")
    print(f"Source: {args.source}")
    if args.filter_priority:
        print(f"Priority filter: {args.filter_priority}")
    if args.dry_run:
        print("Mode: DRY RUN (no issues will be created)")
    print()
    
    # Initialize GitHub client
    try:
        client = GitHubClient(config.repo)
        print("✓ GitHub CLI authenticated")
    except RuntimeError as e:
        print(f"❌ {e}")
        return 1
    
    print()
    
    # Initialize tracker
    tracking_file = config.get_tracking_file()
    tracker = IssueTracker(tracking_file)
    print(f"✓ Tracking file: {tracking_file}")
    print()
    
    # Load issues
    if args.source == 'json':
        issues = load_issues_from_json(config, args.filter_priority)
    else:  # log
        issues = load_issues_from_log(config)
        if args.filter_priority:
            issues = filter_issues_by_priority(issues, args.filter_priority)
            print(f"✓ Filtered to {len(issues)} {args.filter_priority} priority issues")
    
    print()
    
    if not issues:
        print("No issues found to create.")
        return 0
    
    # Filter out already created issues
    issues_to_create = []
    for idx, issue in enumerate(issues):
        issue_id = issue.get('id', f"ISSUE-{idx}")
        if not tracker.is_created(issue_id):
            issues_to_create.append(issue)
    
    already_created_count = len(issues) - len(issues_to_create)
    
    if already_created_count > 0:
        print(f"ℹ️  {already_created_count} issues already created, skipping")
        print()
    
    if not issues_to_create:
        print("✓ All issues have already been created!")
        return 0
    
    print(f"Creating {len(issues_to_create)} issues...")
    print()
    
    # Create issues
    created, failed = create_issues(
        client,
        tracker,
        issues_to_create,
        dry_run=args.dry_run,
        rate_limit_delay=args.rate_limit
    )
    
    # Print summary
    print_summary(created, failed, len(issues_to_create), args.dry_run)
    
    if not args.dry_run:
        print(f"✓ Tracking data saved to: {tracking_file}")
        print()
        print("✓ Issue creation complete!")
        print()
        print("Next steps:")
        print("  1. Review created issues at https://github.com/{config.repo}/issues")
        print("  2. Assign issues to team members")
        print("  3. Add to project board if needed")
        print("  4. Start with critical priority issues")
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
