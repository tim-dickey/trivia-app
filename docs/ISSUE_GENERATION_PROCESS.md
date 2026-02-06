# GitHub Issue Generation Process

## Overview

This document describes the complete process for generating GitHub issues from JSON files, supporting all 4 priority levels (P0-P3).

## Priority Levels

| Priority | Label | Impact | Examples |
|----------|-------|--------|----------|
| **P0** | critical | System-breaking, blocks development | Security vulnerabilities, data loss, deploy blockers |
| **P1** | high | Important features/fixes needed soon | Core functionality gaps, significant bugs |
| **P2** | medium | Improvements and enhancements | Code refactoring, tech debt, non-critical features |
| **P3** | low | Nice-to-have improvements | Optimizations, documentation, UX enhancements |

## JSON File Structure

Each JSON file must contain:

```json
{
  "source": "Code Review 2026-02-02",
  "total_issues": 5,
  "categories": {
    "P0_critical": 5
  },
  "issues": [
    {
      "id": "P0-1",
      "title": "[P0] Issue Title",
      "priority": "critical",
      "labels": ["priority:critical", "category1", "category2"],
      "effort_hours": 8,
      "body": "Issue description in Markdown"
    }
  ]
}
```

### Required Fields

- **id**: Unique identifier (e.g., P0-1, P3-5)
- **title**: Issue title (should include priority prefix)
- **priority**: One of: `critical`, `high`, `medium`, `low`
- **labels**: Array of GitHub labels
- **body**: Full issue description (Markdown format)

## File Organization

```
_bmad-output/implementation-artifacts/
├── code-review-issues-p0.json      # 5 critical issues
├── code-review-issues-p1.json      # 5 high-priority issues
├── code-review-issues-p2.json      # 5 medium-priority issues
├── code-review-issues-p3.json      # 5 low-priority issues
└── code-review-issues-tracking.md  # Generated after creation
```

## Running Issue Creation

### Prerequisites

1. **GitHub CLI installed**: `brew install gh` or `winget install gh`
2. **Authenticated**: `gh auth login`
3. **All JSON files present**: P0-P3 issue files

### Execution

```bash
# Method 1: Using shell script
cd trivia-app/scripts
./run-issue-creation.sh

# Method 2: Direct Python execution
cd trivia-app
python3 scripts/create-github-issues.py
```

### Output

The script provides:

1. **Console Output**: Progress updates and summary
2. **Tracking File**: `code-review-issues-tracking.md` with all created issue numbers

## Acceptance Criteria

### All Issues Must Include

- [ ] Unique ID (P0-1, P1-3, etc.)
- [ ] Priority-prefixed title ([P0], [P1], etc.)
- [ ] Valid priority level
- [ ] At least 2 labels
- [ ] Complete body description (150+ characters)
- [ ] Clear acceptance criteria

## Testing

```bash
cd trivia-app
python3 -m pytest scripts/test_create_github_issues.py -v
```

## Troubleshooting

### Issue: "gh CLI not found"

```bash
# Install GitHub CLI
brew install gh        # macOS
winget install gh      # Windows
curl -sL https://cli.github.com/install.sh | sudo bash  # Linux
```

### Issue: "Not authenticated"

```bash
gh auth login
```

### Issue: "JSON file not found"

Verify file exists: `ls _bmad-output/implementation-artifacts/code-review-issues-*.json`

## Best Practices

1. Review JSON files before creation
2. Test with 1-2 issues first (edit JSON)
3. Keep tracking file updated as work progresses
4. Group related issues in sprints
5. Close duplicates if found
