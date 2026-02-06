# Code Review Process Implementation Guide

## Quick Start: Converting a Code Review to GitHub Issues

This guide walks through the complete process of converting a code review into GitHub issues.

## Step-by-Step Process

### Phase 1: Conduct Code Review (Manual)

**Deliverable**: `code-review-YYYY-MM-DD.md`

1. Review the GitHub PR thoroughly
2. Identify findings by severity:
   - **P0**: Blocks development, security risk, compliance issue
   - **P1**: Important feature/fix needed soon
   - **P2**: Improvements, technical debt, documentation
   - **P3**: Nice-to-have optimizations
3. Document in standard format (see Example section)

**Example Structure**:
```markdown
# Code Review: PR #20

## Executive Summary
[Brief summary of findings]

## PR Scope Analysis
[What was changed]

## Critical Issues (P0)
### Issue Name
- Problem: ...
- Impact: ...
- Recommendation: ...

## High Priority Issues (P1)
[Similar structure]
```

**Reference**: See [code-review-2026-02-02.md](../implementation-artifacts/code-review-2026-02-02.md)

---

### Phase 2: Create JSON Issue Files (Manual)

**Deliverables**: 
- `code-review-issues-p0.json`
- `code-review-issues-p1.json`
- `code-review-issues-p2.json`
- `code-review-issues-p3.json` (optional)

#### Steps:

1. **Create file**: `code-review-issues-pX.json` where X is 0-3

2. **Use schema template**:
   ```json
   {
     "source": "Code Review 2026-02-02",
     "priority_level": "P0",
     "priority_description": "Critical - System-breaking issues",
     "total_issues": 5,
     "issues": []
   }
   ```

3. **For each issue, add**:
   ```json
   {
     "id": "P0-1",
     "title": "[P0] Issue Title Here",
     "priority": "critical",
     "labels": ["priority:critical", "category1", "category2"],
     "effort_hours": 3,
     "body": "## Problem\n\n...\n\n## Acceptance Criteria\n- [ ] Criterion 1\n- [ ] Criterion 2"
   }
   ```

4. **Validation checklist**:
   - [ ] Title starts with [P0]
   - [ ] Priority field is "critical"
   - [ ] At least 2 labels
   - [ ] Effort is positive number
   - [ ] Body has all sections
   - [ ] At least 2 acceptance criteria

**Reference**: See [CODE_REVIEW_JSON_SCHEMA.md](CODE_REVIEW_JSON_SCHEMA.md)

---

### Phase 3: Validate JSON Files (Automated)

**Command**:
```bash
cd trivia-app
python3 -m pytest tests/test_code_review_workflow.py -v
```

**Expected Output**:
```
tests/test_code_review_workflow.py::TestP0Issues::test_p0_file_exists PASSED
tests/test_code_review_workflow.py::TestP0Issues::test_p0_valid_json PASSED
...
======================== 23 passed ========================
```

**If tests fail**:
1. Read error message carefully
2. Fix issue in JSON file
3. Re-run tests
4. Verify all pass before proceeding

---

### Phase 4: Create GitHub Issues (Automated)

**Prerequisites**:
- [ ] GitHub CLI installed: `gh version`
- [ ] Authenticated: `gh auth login`
- [ ] All JSON files validated (Phase 3 complete)

**Command**:
```bash
cd trivia-app
python3 scripts/create-github-issues.py
```

**What happens**:
1. Loads all 4 JSON files (P0-P3)
2. Creates GitHub issue for each entry
3. Applies labels automatically
4. Generates tracking file
5. Shows summary with issue numbers

**Verify in GitHub**:
1. Navigate to GitHub Issues tab
2. Filter by label: `priority:critical`, `priority:high`, etc.
3. Verify all issues created with correct titles and labels
4. Click issue to verify body content renders correctly

---

### Phase 5: Document & Archive (Manual)

**Save tracking file**:
- File: `code-review-issues-tracking.md` (auto-generated)
- Contains: All created issue numbers
- Use to track progress

**Archive artifacts**:
```bash
# Create archive directory
mkdir -p archives/code-reviews/2026-02-02

# Copy all artifacts
cp _bmad-output/implementation-artifacts/code-review-2026-02-02.md archives/code-reviews/2026-02-02/
cp _bmad-output/implementation-artifacts/code-review-issues-p*.json archives/code-reviews/2026-02-02/
cp _bmad-output/implementation-artifacts/code-review-issues-tracking.md archives/code-reviews/2026-02-02/

# Commit
git add archives/
git commit -m "Archive: Code review 2026-02-02 artifacts and issues"
git push
```

**Update CHANGELOG**:
```markdown
## [Unreleased]

### Code Review
- Code review completed for PR #20 (Infrastructure & CI/CD Enhancement)
- 15 GitHub issues created (5 P0, 5 P1, 5 P2)
- See [code-review-issues-tracking.md](link) for progress
```

---

## Common Issues & Solutions

### "JSON Validation Fails"

**Error**: `Issue 1: Missing field 'priority'`

**Solution**:
1. Open the JSON file
2. Find the issue with error
3. Check for typos in field names
4. Ensure priority is lowercase: `"critical"`, not `"Critical"`
5. Re-run tests

### "GitHub Issues Not Created"

**Error**: `gh CLI not found`

**Solution**:
```bash
# Install GitHub CLI
brew install gh        # macOS
winget install gh      # Windows

# Then authenticate
gh auth login
```

### "Title Validation Fails"

**Error**: `Issue 2: Title missing [P#] prefix`

**Solution**:
1. Check title starts with `[P0]`, `[P1]`, etc.
2. Match the priority level
3. Make sure it's uppercase: `[P0]` not `[p0]`

---

## Tips for Success

### Writing Good Issues ✅

- Be specific: "[P0] Implement multi-tenant middleware"
- Use clear problem statement
- Include concrete examples
- Make acceptance criteria testable
- Estimate conservatively

### Labels Strategy

**Always include**:
- `priority:critical|high|medium|low` (required)

**Add relevant**:
- Component: `backend`, `frontend`, `ci/cd`
- Type: `security`, `testing`, `documentation`
- Area: specific feature name

### Effort Estimation

- **P0**: 1-16 hours (avg 5)
- **P1**: 1-8 hours (avg 3.5)
- **P2**: 0.5-3 hours (avg 1)
- **P3**: 2-8 hours (avg 2.5)

---

## Workflow Diagram

```
Code Review (*.md) → JSON Files → Validation → GitHub Issues → Archive
```

## When Things Go Wrong

### Debugging Checklist

If tests fail:
1. [ ] Check JSON syntax
2. [ ] Verify field names correct
3. [ ] Ensure all required fields present
4. [ ] Check priority matches file
5. [ ] Verify title format: [P#] Issue Name
6. [ ] Confirm at least 2 labels
7. [ ] Check body has all sections
8. [ ] Ensure effort is positive number
9. [ ] Verify acceptance criteria format
10. [ ] Run full test suite

### Getting Help

1. **Check documentation**:
   - [CODE_REVIEW_WORKFLOW.md](CODE_REVIEW_WORKFLOW.md)
   - [CODE_REVIEW_JSON_SCHEMA.md](CODE_REVIEW_JSON_SCHEMA.md)
   - [CODE_REVIEW_TEST_RESULTS.md](CODE_REVIEW_TEST_RESULTS.md)

2. **Review examples**:
   - [code-review-issues-p0.json](../implementation-artifacts/code-review-issues-p0.json)
   - [code-review-issues-p1.json](../implementation-artifacts/code-review-issues-p1.json)

3. **Validate manually**:
   ```bash
   python3 -c "import json; json.load(open('code-review-issues-p0.json'))"
   ```

---

## Reference

- [Code Review Workflow](CODE_REVIEW_WORKFLOW.md) - Detailed process flow
- [JSON Schema](CODE_REVIEW_JSON_SCHEMA.md) - Field definitions and validation
- [Test Results](CODE_REVIEW_TEST_RESULTS.md) - Validation test coverage
- [Issue Creation Script](../../scripts/create-github-issues.py) - Implementation
- [Test Suite](../../tests/test_code_review_workflow.py) - Validation tests
