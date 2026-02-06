# Code Review JSON Schema

## Quick Reference

```json
{
  "source": "Code Review 2026-02-02",
  "priority_level": "P0",
  "priority_description": "Critical - System-breaking issues",
  "total_issues": 5,
  "issues": [
    {
      "id": "P0-1",
      "title": "[P0] Consolidate CI/CD Workflows",
      "priority": "critical",
      "labels": ["priority:critical", "ci/cd", "tech-debt"],
      "effort_hours": 3,
      "blocks": ["efficient-development"],
      "body": "## Problem\nDescription\n\n## Impact\nImpact\n\n## Proposed Solution\nSolution\n\n## Acceptance Criteria\n- [ ] Criterion 1\n- [ ] Criterion 2\n\n**Estimated Effort**: 3 hours\n**Priority**: P0\n**Source**: Code Review 2026-02-02"
    }
  ]
}
```

## Field Definitions

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|----------|
| `source` | string | Yes | Source of review | "Code Review 2026-02-02" |
| `priority_level` | string | Yes | P0, P1, P2, or P3 | "P0" |
| `priority_description` | string | Yes | Human-readable description | "Critical - System-breaking issues" |
| `total_issues` | number | Yes | Count of issues in file | 5 |
| `issues` | array | Yes | Array of issue objects | [...] |
| `issues[].id` | string | Yes | Unique ID (P#-N) | "P0-1" |
| `issues[].title` | string | Yes | Title with [P#] prefix | "[P0] Fix CI/CD" |
| `issues[].priority` | string | Yes | critical/high/medium/low | "critical" |
| `issues[].labels` | array | Yes | GitHub labels (min 2) | ["priority:critical", "ci/cd"] |
| `issues[].effort_hours` | number | Yes | Estimated effort (0.25-40) | 3 |
| `issues[].blocks` | array | No | Blocked features | ["mvp-features"] |
| `issues[].body` | string | Yes | Full description (Markdown) | "## Problem..." |

## Validation Rules

### Source Format
- Pattern: `"Code Review YYYY-MM-DD"`
- Example: `"Code Review 2026-02-02"` ✅
- Counter: `"Code Review Feb 2"` ❌

### Priority Level
- Enum: P0, P1, P2, P3
- Must match file type
- All issues in file must match

### Priority Field Mapping
```
P0 → "critical"
P1 → "high"
P2 → "medium"
P3 → "low"
```

### ID Format
- Pattern: `P[0-3]-\d+`
- Examples: P0-1, P1-5, P3-2 ✅
- Invalid: P0-A, 0-1 ❌
- Must be unique across all files
- Sequential within priority: P0-1, P0-2, P0-3...

### Title Format
- Must start with [P0], [P1], [P2], or [P3]
- Length: 10-120 characters
- Match priority of issue
- Example: `"[P0] Consolidate CI/CD Workflows"` ✅
- Invalid: `"Consolidate CI/CD"` ❌ (missing prefix)

### Labels
- Minimum 2 labels required
- First should be priority label:
  - `priority:critical` (P0)
  - `priority:high` (P1)
  - `priority:medium` (P2)
  - `priority:low` (P3)
- Additional by category/component
- Examples:
  - `["priority:critical", "security", "backend"]` ✅
  - `["priority:critical"]` ❌ (insufficient)

### Effort Hours
- Type: number (integer or float)
- Range: 0.25 to 40 hours
- Examples:
  - 0.25 = 15 minutes
  - 0.5 = 30 minutes
  - 1 = 1 hour
  - 3 = 3 hours
  - 8 = 1 day
- Realistic ranges:
  - P0: 1-16 (avg 5)
  - P1: 1-8 (avg 3.5)
  - P2: 0.5-3 (avg 1)
  - P3: 2-8 (avg 2.5)

### Body Content
- Minimum 150 characters
- Markdown format
- Required sections (in order):
  ```markdown
  ## Problem
  [Description of problem]
  
  ## Impact
  [Business/technical impact]
  
  ## Proposed Solution
  [Recommended approach]
  
  ## Acceptance Criteria
  - [ ] Criterion 1
  - [ ] Criterion 2
  ```
- Optional sections:
  ```markdown
  ## Implementation Details
  [Link to action items or specs]
  
  **Estimated Effort**: X hours
  **Priority**: P0 - [Reason]
  **Source**: Code Review YYYY-MM-DD
  ```

### Blocks Field
- Type: array (optional)
- Elements: strings (feature names)
- Only include if issue blocks something
- Example: `["mvp-features", "session-management"]`

## Complete Example (Valid)

```json
{
  "source": "Code Review 2026-02-02",
  "priority_level": "P0",
  "priority_description": "Critical - System-breaking issues blocking development",
  "total_issues": 5,
  "issues": [
    {
      "id": "P0-1",
      "title": "[P0] Consolidate CI/CD Workflows to Eliminate Duplicate Test Runs",
      "priority": "critical",
      "labels": ["priority:critical", "ci/cd", "tech-debt"],
      "effort_hours": 3,
      "blocks": ["efficient-development"],
      "body": "## Problem\n\nCurrently, both Codacy and CodeQL workflows run tests on every PR, causing duplicate test execution and wasting CI/CD minutes.\n\n## Impact\n\n- Efficiency: CI runs take 2x longer than necessary\n- Cost: Wastes GitHub Actions minutes\n- Developer Experience: Slower feedback on PRs\n\n## Proposed Solution\n\nCreate a consolidated CI workflow structure where tests run once and results are uploaded to both Codacy and GitHub security tools.\n\n## Acceptance Criteria\n\n- [ ] Single workflow runs tests on PRs\n- [ ] No duplicate test executions\n- [ ] Coverage reports uploaded to Codacy and GitHub\n- [ ] PR feedback time reduced by 50%\n\n**Estimated Effort**: 3 hours\n**Priority**: P0 - Blocks efficient development\n**Source**: Code Review 2026-02-02"
    },
    {
      "id": "P0-2",
      "title": "[P0] Implement Organization Scoping Middleware for Multi-Tenancy",
      "priority": "critical",
      "labels": ["priority:critical", "security", "multi-tenancy", "backend"],
      "effort_hours": 8,
      "blocks": ["feature-development", "data-security"],
      "body": "## Problem\n\nMulti-tenant data isolation is not enforced at the application layer. No middleware to automatically filter by organization_id.\n\n## Impact\n\n- Security Risk: HIGH - Data could leak between tenants\n- Compliance: GDPR and SOC 2 violations possible\n- Development: Manual filtering required on every query\n\n## Proposed Solution\n\nImplement organization scoping middleware that extracts organization from JWT and automatically filters all queries.\n\n## Acceptance Criteria\n\n- [ ] Middleware extracts organization from JWT\n- [ ] Base CRUD class auto-filters by organization_id\n- [ ] Integration tests validate tenant isolation\n- [ ] No queries bypass organization filter\n\n**Estimated Effort**: 8 hours\n**Priority**: P0 - Security critical\n**Source**: Code Review 2026-02-02"
    }
  ]
}
```

## Common Mistakes

### Mistake 1: Wrong Priority Field Value
```json
// ❌ WRONG
{"priority": "Critical"}  // Not lowercase
{"priority": "critical-high"}  // Invalid enum

// ✅ CORRECT
{"priority": "critical"}  // Lowercase
```

### Mistake 2: Missing Priority Prefix in Title
```json
// ❌ WRONG
{"title": "Consolidate CI/CD Workflows"}  // No [P0]

// ✅ CORRECT  
{"title": "[P0] Consolidate CI/CD Workflows"}  // Has [P0]
```

### Mistake 3: Insufficient Labels
```json
// ❌ WRONG
{"labels": ["priority:critical"]}  // Only 1 label

// ✅ CORRECT
{"labels": ["priority:critical", "ci/cd", "tech-debt"]}  // 3 labels
```

### Mistake 4: Mismatched Priority
```json
// In P0 file:
// ❌ WRONG
{"priority": "high"}  // Doesn't match P0

// ✅ CORRECT
{"priority": "critical"}  // Matches P0
```

### Mistake 5: Insufficient Acceptance Criteria
```json
// ❌ WRONG
{"body": "## Acceptance Criteria\n- [ ] Do something"}  // Only 1 criterion

// ✅ CORRECT
{"body": "## Acceptance Criteria\n- [ ] Criterion 1\n- [ ] Criterion 2"}  // 2+ criteria
```

### Mistake 6: Out-of-Range Effort
```json
// ❌ WRONG
{"effort_hours": 0.1}  // Below minimum 0.25
{"effort_hours": 100}  // Above maximum 40

// ✅ CORRECT
{"effort_hours": 0.5}  // 30 minutes
{"effort_hours": 8}  // 1 day
```

## Cross-File Validation

### No Duplicate IDs
```
P0-1, P0-2, P0-3, P0-4, P0-5 (all unique) ✅
P0-1, P0-2, P0-1 (duplicate!) ❌
```

### Sequential Numbering
```
P0: P0-1, P0-2, P0-3, P0-4, P0-5 ✅
P0: P0-1, P0-3, P0-5 (gaps) ❌
```

### Total Issues
```
File: code-review-issues-p0.json
Total issues field: 5
Actual issues: 5 ✅

Total issues field: 5
Actual issues: 4 ❌
```

## Validation Tools

### Using Python
```python
import json
from jsonschema import validate, ValidationError

# Load file
with open('code-review-issues-p0.json') as f:
    data = json.load(f)

# Validate
if len(data['issues']) != data['total_issues']:
    print('❌ Count mismatch')
else:
    print('✅ Count matches')

for issue in data['issues']:
    if not issue['title'].startswith('[P'):
        print(f'❌ Missing prefix: {issue["id"]}')
```

### Online Tools
- [JSON Validator](https://jsonformatter.org/)
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)

## Testing Checklist

Before creating GitHub issues:

- [ ] All JSON files exist (P0-P3)
- [ ] All JSON files are valid
- [ ] All required fields present
- [ ] Priority matches file (P0→critical)
- [ ] Titles have [P#] prefix
- [ ] At least 2 labels per issue
- [ ] Effort within valid range
- [ ] Body has all sections
- [ ] At least 2 acceptance criteria
- [ ] No duplicate IDs
- [ ] Sequential numbering
- [ ] Total count matches
- [ ] Test suite passes (pytest)

## References

- [Workflow Documentation](CODE_REVIEW_WORKFLOW.md)
- [Test Suite](../tests/test_code_review_workflow.py)
- [Test Results](CODE_REVIEW_TEST_RESULTS.md)
