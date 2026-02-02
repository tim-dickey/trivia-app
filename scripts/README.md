# Issue Creation Scripts

This directory contains automation scripts for creating GitHub issues from collected issue data.

## Available Scripts

### 1. create-issues-from-log.py (RECOMMENDED)

**New in 2026-02-02**: Works with the consolidated issues log.

Creates GitHub issues from the consolidated `issues-log.json` file which includes all issues from multiple sources (code review, PRD validation, etc.).

**Features**:
- Creates issues from consolidated log (20 issues total)
- Tracks created issues by updating the log file
- Skips already-created issues
- Updates GitHub issue numbers in the log
- Shows detailed progress and summary

**Usage**:
```bash
# Authenticate once
gh auth login

# Create all issues from the log
python3 scripts/create-issues-from-log.py
```

**Input**: `_bmad-output/implementation-artifacts/issues-log.json`  
**Output**: Updates the same file with GitHub issue numbers

---

### 2. create-github-issues.py (Original)

Creates GitHub issues from the original code review JSON files (P0, P1, P2).

**Features**:
- Creates 15 code review issues
- Validates JSON structure
- Generates tracking file

**Usage**:
```bash
gh auth login
python3 scripts/create-github-issues.py
```

**Input**: `code-review-issues-p0.json`, `code-review-issues-p1.json`, `code-review-issues-p2.json`  
**Output**: `code-review-issues-tracking.md`

---

### 3. create-code-review-issues.sh

Bash alternative for creating code review issues. Contains individual functions for each issue.

**Usage**:
```bash
gh auth login
bash scripts/create-code-review-issues.sh
```

---

### 4. run-issue-creation.sh

Wrapper script that calls the Python automation with proper setup.

**Usage**:
```bash
bash scripts/run-issue-creation.sh
```

---

## Comparison

| Script | Issues | Source | Tracking | Best For |
|--------|--------|--------|----------|----------|
| **create-issues-from-log.py** | 20 | Consolidated log | Updates log file | **Most up-to-date, recommended** |
| create-github-issues.py | 15 | Code review JSONs | Separate tracking file | Code review issues only |
| create-code-review-issues.sh | 15 | Inline bash | Manual | Bash users, selective creation |
| run-issue-creation.sh | 15 | Via Python | Via Python script | Simple wrapper |

## Recommended Workflow

### First Time Setup
```bash
# 1. Authenticate with GitHub CLI
gh auth login

# 2. Create all issues from consolidated log
python3 scripts/create-issues-from-log.py
```

### After Issues Are Created
The `issues-log.json` file will be automatically updated with:
- GitHub issue numbers
- Creation dates
- Status changes
- Summary statistics

### Re-running the Script
The script is **idempotent** - it will:
- Skip already-created issues (checks `github_issue_number` field)
- Only create new/pending issues
- Show which issues are already created

Example output:
```
ℹ️  15 issues already created, skipping:
   - LOG-001: #23 [P0] Consolidate CI/CD Workflows
   - LOG-002: #24 [P0] Organization Scoping Middleware
   ...

Creating 5 new issues...
```

## Issue Log Structure

The consolidated log includes:
- **20 total issues**
  - 15 from Code Review 2026-02-02
  - 5 from PRD Validation 2026-01-24
- **Priorities**: 5 P0 (Critical), 5 P1 (High), 10 P2 (Medium)
- **Total Effort**: 5.4 days (43 hours)

## Troubleshooting

### "gh CLI not found"
```bash
# Install GitHub CLI
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

### "Not authenticated"
```bash
gh auth login
# Follow the prompts to authenticate
```

### "Issues already exist"
Check if issues were created manually:
```bash
gh issue list --repo tim-dickey/trivia-app
```

If needed, update the log manually:
```bash
# Edit issues-log.json and set github_issue_number for existing issues
```

### Script fails partway through
The script saves progress after each issue. Just re-run it:
```bash
python3 scripts/create-issues-from-log.py
# Will skip already-created issues and continue
```

## Advanced Usage

### Query the Issues Log
```bash
# Get all critical issues
jq '.issues[] | select(.priority == "critical")' _bmad-output/implementation-artifacts/issues-log.json

# Get issues by category
jq '.issues[] | select(.category == "security")' _bmad-output/implementation-artifacts/issues-log.json

# Get summary statistics
jq '.summary' _bmad-output/implementation-artifacts/issues-log.json

# Find quick wins (< 1 hour)
jq '.issues[] | select(.effort_hours <= 1) | {id, title, effort_hours}' _bmad-output/implementation-artifacts/issues-log.json
```

### Create Issues Selectively
Edit `create-issues-from-log.py` to filter issues:
```python
# Example: Only create P0 issues
issues_to_create = [i for i in issues if i['priority'] == 'critical']
```

### Export to CSV
```bash
python3 << 'EOF'
import json
import csv

with open('_bmad-output/implementation-artifacts/issues-log.json') as f:
    data = json.load(f)

with open('issues.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Title', 'Priority', 'Category', 'Effort (hours)', 'Status'])
    for issue in data['issues']:
        writer.writerow([
            issue['issue_id'],
            issue['title'],
            issue['priority'],
            issue['category'],
            issue['effort_hours'],
            issue['status']
        ])
print("Exported to issues.csv")
EOF
```

## Documentation

- **Issues Log**: `_bmad-output/implementation-artifacts/issues-log.md` - Human-readable
- **Issues Log JSON**: `_bmad-output/implementation-artifacts/issues-log.json` - Machine-readable
- **Creation Guide**: `_bmad-output/implementation-artifacts/issues-creation-guide.md` - Detailed guide
- **Main Instructions**: `/ISSUE_CREATION_INSTRUCTIONS.md` - User-facing instructions

---

**Maintained By**: Development Team  
**Last Updated**: 2026-02-02
