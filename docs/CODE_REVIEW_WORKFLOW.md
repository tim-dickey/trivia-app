# Code Review to GitHub Issues Workflow

## Overview

This document formalizes the process for converting code review findings into structured GitHub issues across all 4 priority levels (P0-P3).

## Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CONDUCT CODE REVIEW                                          │
│    └─ Review PR #X                                              │
│    └─ Identify findings by severity (P0-P3)                     │
│    └─ Document in code-review-YYYY-MM-DD.md                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│ 2. CATEGORIZE FINDINGS                                          │
│    └─ P0 (Critical): Blocks development/security risk           │
│    └─ P1 (High): Important features/fixes needed soon           │
│    └─ P2 (Medium): Improvements and enhancements                │
│    └─ P3 (Low): Nice-to-have improvements                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│ 3. GENERATE JSON ISSUE FILES                                    │
│    └─ code-review-issues-p0.json (5 issues per file)            │
│    └─ code-review-issues-p1.json                                │
│    └─ code-review-issues-p2.json                                │
│    └─ code-review-issues-p3.json                                │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│ 4. VALIDATE JSON STRUCTURE                                      │
│    └─ Validate against schema                                   │
│    └─ Run test suite                                            │
│    └─ Verify all required fields                                │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│ 5. CREATE GITHUB ISSUES                                         │
│    └─ Run create-github-issues.py                               │
│    └─ Generate tracking file                                    │
│    └─ Link to code review document                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│ 6. DOCUMENT & TRACK                                             │
│    └─ Save code-review-issues-tracking.md                       │
│    └─ Update CHANGELOG                                          │
│    └─ Link from project board                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Priority Definitions

| Priority | Level | Impact | Examples |
|----------|-------|--------|----------|
| **P0** | Critical | System-breaking, blocks development or security | Security vulnerabilities, data loss, deploy blockers |
| **P1** | High | Important features/fixes needed soon | Core functionality gaps, significant bugs, missing MVP features |
| **P2** | Medium | Improvements and enhancements | Code refactoring, tech debt, documentation |
| **P3** | Low | Nice-to-have improvements | Optimizations, developer experience, suggestions |

## Schema Overview

```json
{
  "source": "Code Review YYYY-MM-DD",
  "priority_level": "P0|P1|P2|P3",
  "priority_description": "Description",
  "total_issues": 5,
  "issues": [
    {
      "id": "P0-1",
      "title": "[P0] Issue Title",
      "priority": "critical|high|medium|low",
      "labels": ["priority:critical", "category"],
      "effort_hours": 3,
      "blocks": ["optional"],
      "body": "## Problem\n...\n## Acceptance Criteria\n- [ ] Criterion 1"
    }
  ]
}
```

## Validation Rules

### File-Level
- Source: "Code Review YYYY-MM-DD" format
- Priority level: P0, P1, P2, or P3
- Total issues: 5 per file
- Valid JSON format

### Issue-Level
- ID: Format P#-N (P0-1, P1-2, etc.)
- Title: Must start with [P#] prefix
- Priority: Must be lowercase (critical, high, medium, low)
- Labels: Minimum 2, must include priority:X
- Effort: Between 0.25-40 hours
- Body: Must include Problem, Impact, Solution, Acceptance Criteria (2+ items)

### Cross-File
- No duplicate IDs
- Sequential numbering within priority
- All 4 files created

## Testing

Run validation test suite:
```bash
python3 -m pytest tests/test_code_review_workflow.py -v
```

Expected: 23+ tests passing (92%+ success rate)

See [Test Results](CODE_REVIEW_TEST_RESULTS.md) for detailed results.

## Effort Estimates

**P0**: 1-16 hours (avg 5)
**P1**: 1-8 hours (avg 3.5)
**P2**: 0.5-3 hours (avg 1)
**P3**: 2-8 hours (avg 2.5)

## References

- [JSON Schema Documentation](CODE_REVIEW_JSON_SCHEMA.md)
- [Process Implementation Guide](CODE_REVIEW_PROCESS_GUIDE.md)
- [Test Results](CODE_REVIEW_TEST_RESULTS.md)
- [Example Code Review](../_bmad-output/implementation-artifacts/code-review-2026-02-02.md)
