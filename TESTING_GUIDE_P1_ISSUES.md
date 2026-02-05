# Testing Guide: P1 Issue Creation Process

This guide provides step-by-step instructions for testing the P1 issue creation automation.

## Prerequisites

Before testing, ensure you have:
- ✅ Git installed
- ✅ Python 3.6+ installed
- ✅ GitHub CLI (`gh`) installed (https://cli.github.com/)
- ✅ Access to the repository: `tim-dickey/trivia-app`

## Test Environment Setup

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone https://github.com/tim-dickey/trivia-app.git
cd trivia-app

# Checkout the P1 issues branch
git fetch origin
git checkout copilot/create-issue-records-p1
git pull origin copilot/create-issue-records-p1
```

### 2. Verify Files Exist

```bash
# Check that all required files are present
ls -la scripts/create-p1-issues*.py scripts/create-p1-issues*.sh
ls -la _bmad-output/implementation-artifacts/code-review-issues-p1.json
ls -la _bmad-output/implementation-artifacts/P1_ISSUES_TO_CREATE.md
```

Expected output: All files should be listed without errors.

## Testing Methods

### Method 1: Automated Testing (Using Python Script)

#### Step 1: Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate.

#### Step 2: Verify Authentication

```bash
gh auth status
```

Expected output: Should show you're logged in as your GitHub username.

#### Step 3: Run the Script

```bash
python3 scripts/create-p1-issues.py
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║               Creating P1 GitHub Issues from JSON File                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Repository: tim-dickey/trivia-app
Source File: /path/to/_bmad-output/implementation-artifacts/code-review-issues-p1.json

✓ GitHub CLI authenticated
✓ Loaded 5 P1 issues from JSON file

Creating 5 new P1 issues...

Creating: [P1] Update Outdated Dependencies with Security Patches
✓ Created: https://github.com/tim-dickey/trivia-app/issues/XX

Creating: [P1] Add Frontend CI Workflow for Quality Validation
✓ Created: https://github.com/tim-dickey/trivia-app/issues/XX

Creating: [P1] Expand CodeQL Security Analysis to Python and TypeScript
✓ Created: https://github.com/tim-dickey/trivia-app/issues/XX

Creating: [P1] Add Application Services to Docker Compose
✓ Created: https://github.com/tim-dickey/trivia-app/issues/XX

Creating: [P1] Add Security Headers Middleware
✓ Created: https://github.com/tim-dickey/trivia-app/issues/XX

✓ Successfully created 5/5 issues
✓ Tracking file updated: _bmad-output/implementation-artifacts/p1-issues-created.json
```

#### Step 4: Verify in GitHub Web UI

1. Open: https://github.com/tim-dickey/trivia-app/issues
2. Verify 5 new issues are visible
3. Check each issue has:
   - ✅ Correct title (starts with `[P1]`)
   - ✅ `priority:high` label
   - ✅ Additional labels (security, ci/cd, etc.)
   - ✅ Complete body with acceptance criteria
   - ✅ Open state

#### Step 5: Test Idempotency (Re-run Protection)

```bash
# Run the script again
python3 scripts/create-p1-issues.py
```

**Expected Output:**
```
ℹ️  5 issues already created, skipping:
   - P1-1: #XX [P1] Update Outdated Dependencies with Security Patches
   - P1-2: #XX [P1] Add Frontend CI Workflow for Quality Validation
   - P1-3: #XX [P1] Expand CodeQL Security Analysis to Python and TypeScript
   - P1-4: #XX [P1] Add Application Services to Docker Compose
   - P1-5: #XX [P1] Add Security Headers Middleware

✓ All issues have already been created!
```

### Method 2: Testing with Direct Script (Alternative)

```bash
python3 scripts/create-p1-issues-direct.py
```

This script has three behaviors to test:

**Test Case A: With gh CLI Authentication**
- Prerequisite: `gh auth login` completed
- Expected: Creates all 5 issues (same as Method 1)

**Test Case B: With GITHUB_TOKEN**
```bash
export GITHUB_TOKEN="your_token_here"
python3 scripts/create-p1-issues-direct.py
```
- Expected: Creates issues using GitHub API directly

**Test Case C: No Authentication**
```bash
# Logout first
gh auth logout

# Run without token
python3 scripts/create-p1-issues-direct.py
```
- Expected: Creates markdown file with all issues
- Verify: `_bmad-output/implementation-artifacts/P1_ISSUES_TO_CREATE.md` is generated/updated

### Method 3: Testing Bash Script

```bash
./scripts/create-p1-issues.sh
```

Expected output: Similar to Python script with colored output.

### Method 4: Manual Creation Testing

1. Open `_bmad-output/implementation-artifacts/P1_ISSUES_TO_CREATE.md`
2. For each issue (1-5):
   - Visit https://github.com/tim-dickey/trivia-app/issues/new
   - Copy title from markdown
   - Add labels (comma-separated)
   - Copy body content
   - Submit issue
3. Verify all 5 issues created correctly

## Verification Checklist

After running any test method, verify:

### Issue Content Verification

For each of the 5 created issues:

- [ ] **Issue 1: Update Outdated Dependencies**
  - Title: `[P1] Update Outdated Dependencies with Security Patches`
  - Labels: priority:high, security, dependencies, backend, frontend
  - Body contains: Problem, Security Impact, Proposed Solution, Acceptance Criteria
  - Effort: 4 hours mentioned

- [ ] **Issue 2: Frontend CI Workflow**
  - Title: `[P1] Add Frontend CI Workflow for Quality Validation`
  - Labels: priority:high, ci/cd, frontend, testing
  - Body contains: Problem, Proposed Solution, Acceptance Criteria
  - Effort: 2 hours mentioned

- [ ] **Issue 3: Expand CodeQL**
  - Title: `[P1] Expand CodeQL Security Analysis to Python and TypeScript`
  - Labels: priority:high, security, ci/cd, codeql
  - Body contains: Problem, Security Gap, Proposed Solution, Security Benefits, Acceptance Criteria
  - Effort: 1 hour mentioned

- [ ] **Issue 4: Docker Compose Services**
  - Title: `[P1] Add Application Services to Docker Compose`
  - Labels: priority:high, docker, developer-experience, infrastructure
  - Body contains: Problem, Proposed Solution, Acceptance Criteria
  - Effort: 3 hours mentioned

- [ ] **Issue 5: Security Headers**
  - Title: `[P1] Add Security Headers Middleware`
  - Labels: priority:high, security, backend, middleware
  - Body contains: Problem, Security Risk, Security Best Practices, Proposed Solution, Acceptance Criteria
  - Effort: 2 hours mentioned

### Tracking File Verification

```bash
# Check tracking file was created
cat _bmad-output/implementation-artifacts/p1-issues-created.json
```

Expected: JSON file with all 5 issues, including GitHub issue numbers.

### GitHub API Verification

```bash
# Verify via GitHub CLI
gh issue list --repo tim-dickey/trivia-app --label priority:high --limit 10
```

Expected: All 5 P1 issues listed.

## Error Testing

### Test Error Handling

#### Test 1: Missing JSON File
```bash
# Rename the source file
mv _bmad-output/implementation-artifacts/code-review-issues-p1.json /tmp/backup.json

# Run script
python3 scripts/create-p1-issues.py

# Restore file
mv /tmp/backup.json _bmad-output/implementation-artifacts/code-review-issues-p1.json
```
**Expected:** Error message about missing file.

#### Test 2: Invalid JSON
```bash
# Backup original
cp _bmad-output/implementation-artifacts/code-review-issues-p1.json /tmp/backup.json

# Create invalid JSON
echo "{invalid json" > _bmad-output/implementation-artifacts/code-review-issues-p1.json

# Run script
python3 scripts/create-p1-issues.py

# Restore
mv /tmp/backup.json _bmad-output/implementation-artifacts/code-review-issues-p1.json
```
**Expected:** Error message about malformed JSON.

#### Test 3: Not Authenticated
```bash
# Logout
gh auth logout

# Run script
python3 scripts/create-p1-issues.py
```
**Expected:** Error asking to authenticate.

## Performance Testing

Time the script execution:

```bash
time python3 scripts/create-p1-issues.py
```

**Expected Duration:** 5-15 seconds (depending on network speed)
- ~1 second per issue creation
- Rate limiting delays included

## Cross-Platform Testing

### Windows Testing

```powershell
# PowerShell commands
python scripts/create-p1-issues.py
```

### macOS/Linux Testing

```bash
# Bash commands
python3 scripts/create-p1-issues.py
./scripts/create-p1-issues.sh
```

## Cleanup After Testing

To remove test issues (if needed):

```bash
# List created issues
gh issue list --repo tim-dickey/trivia-app --label priority:high

# Close issues (replace XX with issue numbers)
gh issue close XX --repo tim-dickey/trivia-app
```

Or delete the tracking file to allow re-creation:
```bash
rm _bmad-output/implementation-artifacts/p1-issues-created.json
```

## Troubleshooting

### Issue: Script not found
**Solution:** Make sure you're in the repository root and have pulled the latest changes.

### Issue: Permission denied
**Solution:** Make scripts executable:
```bash
chmod +x scripts/create-p1-issues.py scripts/create-p1-issues.sh
```

### Issue: gh command not found
**Solution:** Install GitHub CLI from https://cli.github.com/

### Issue: Issues not appearing in GitHub
**Solution:** 
1. Refresh the browser
2. Check you're viewing the correct repository
3. Verify issues weren't created in a fork

## Success Criteria

Testing is successful when:
1. ✅ All 5 P1 issues created without errors
2. ✅ Each issue has correct title, labels, and body
3. ✅ Tracking file generated successfully
4. ✅ Re-running script shows idempotency (no duplicates)
5. ✅ Issues visible at https://github.com/tim-dickey/trivia-app/issues
6. ✅ Error handling works correctly for invalid inputs

## Test Report Template

After testing, document results:

```
Test Date: [DATE]
Tester: [NAME]
Branch: copilot/create-issue-records-p1
Commit: [COMMIT_HASH]

Method Tested: [Python/Bash/Manual]
Authentication: [gh CLI/Token/None]

Results:
- Issues Created: [X/5]
- Time Taken: [XX seconds]
- Errors Encountered: [None/Details]
- Idempotency Test: [Pass/Fail]
- Label Verification: [Pass/Fail]
- Content Verification: [Pass/Fail]

Overall Status: [✅ PASS / ❌ FAIL]

Notes:
[Any additional observations]
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-05  
**Maintained By:** Development Team
