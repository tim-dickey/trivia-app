# Issue Format Schema and Guardrails

**Purpose**: Define the expected format for all GitHub issues created from `_bmad-output/implementation-artifacts/`  
**Version**: 1.0  
**Last Updated**: 2026-02-12  
**Authority**: Based on scripts refactor and all-issues-to-create.md

---

## Table of Contents

1. [JSON Schema Definition](#json-schema-definition)
2. [Root Object Structure](#root-object-structure)
3. [Issue Object Structure](#issue-object-structure)
4. [Field Requirements](#field-requirements)
5. [Priority Levels](#priority-levels)
6. [Body Format Specification](#body-format-specification)
7. [Label Format](#label-format)
8. [Validation Rules](#validation-rules)
9. [Examples by Priority](#examples-by-priority)
10. [Migration Guide](#migration-guide)

---

## JSON Schema Definition

### Complete JSON Schema (v1.0)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GitHub Issues JSON Format",
  "description": "Schema for code review and implementation issues",
  "type": "object",
  "required": ["source", "total_issues", "issues"],
  "properties": {
    "source": {
      "type": "string",
      "description": "Source of the issues (e.g., 'Code Review 2026-02-02')",
      "pattern": "^.{5,100}$"
    },
    "total_issues": {
      "type": "integer",
      "description": "Total number of issues in this file",
      "minimum": 0
    },
    "categories": {
      "type": "object",
      "description": "Breakdown of issues by category (optional)",
      "additionalProperties": {
        "type": "integer",
        "minimum": 0
      }
    },
    "priority_level": {
      "type": "string",
      "description": "Priority level identifier (optional, P3 only)",
      "enum": ["P0", "P1", "P2", "P3"]
    },
    "priority_description": {
      "type": "string",
      "description": "Human-readable priority description (optional)"
    },
    "issues": {
      "type": "array",
      "description": "Array of issue objects",
      "items": {
        "$ref": "#/definitions/issue"
      }
    }
  },
  "definitions": {
    "issue": {
      "type": "object",
      "required": ["id", "title", "priority", "labels", "effort_hours", "body"],
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique issue identifier",
          "pattern": "^P[0-3]-[0-9]+$"
        },
        "title": {
          "type": "string",
          "description": "Issue title with priority prefix",
          "pattern": "^\\[P[0-3]\\] .{10,200}$"
        },
        "priority": {
          "type": "string",
          "description": "Priority level",
          "enum": ["critical", "high", "medium", "low"]
        },
        "labels": {
          "type": "array",
          "description": "GitHub labels to apply",
          "items": {
            "type": "string",
            "pattern": "^[a-z0-9-:/]+$"
          },
          "minItems": 1,
          "uniqueItems": true
        },
        "effort_hours": {
          "type": "number",
          "description": "Estimated effort in hours",
          "minimum": 0.25,
          "maximum": 80
        },
        "blocks": {
          "type": "array",
          "description": "What this issue blocks (optional, typically P0 only)",
          "items": {
            "type": "string"
          }
        },
        "body": {
          "type": "string",
          "description": "Markdown body with required sections",
          "minLength": 200
        }
      }
    }
  }
}
```

---

## Root Object Structure

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `source` | string | Source/origin of issues | `"Code Review 2026-02-02"` |
| `total_issues` | integer | Total count of issues | `5` |
| `issues` | array | Array of issue objects | `[...]` |

### Optional Fields

| Field | Type | Used In | Description |
|-------|------|---------|-------------|
| `categories` | object | P0, P1, P2 | Breakdown of issues by category |
| `priority_level` | string | P3 | Priority identifier (e.g., "P3") |
| `priority_description` | string | P3 | Human-readable description |

### Examples

**P0/P1/P2 Format**:
```json
{
  "source": "Code Review 2026-02-02",
  "total_issues": 5,
  "categories": {
    "P0_critical": 5
  },
  "issues": [...]
}
```

**P3 Format**:
```json
{
  "source": "Code Review 2026-02-02",
  "priority_level": "P3",
  "priority_description": "Low priority - Nice-to-have improvements and optimizations",
  "total_issues": 5,
  "issues": [...]
}
```

---

## Issue Object Structure

### Required Fields (All Priorities)

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| `id` | string | `^P[0-3]-[0-9]+$` | Unique identifier (e.g., "P0-1") |
| `title` | string | `^\\[P[0-3]\\] .{10,200}$` | Title with priority prefix |
| `priority` | string | `critical\|high\|medium\|low` | Normalized priority level |
| `labels` | array[string] | Min 1, unique | GitHub labels to apply |
| `effort_hours` | number | 0.25 - 80 | Estimated effort in hours |
| `body` | string | Min 200 chars | Markdown body with sections |

### Optional Fields

| Field | Type | Priority | Description |
|-------|------|----------|-------------|
| `blocks` | array[string] | Typically P0 | What this issue blocks |

---

## Field Requirements

### 1. `id` Field

**Format**: `P{priority}-{number}`

**Rules**:
- Priority: 0-3 (0=Critical, 1=High, 2=Medium, 3=Low)
- Number: Sequential, starting from 1
- Pattern: `^P[0-3]-[0-9]+$`

**Examples**:
```
✅ Valid:   P0-1, P1-5, P2-10, P3-3
❌ Invalid: P4-1, P0, P1-A, p1-1
```

### 2. `title` Field

**Format**: `[P{priority}] {descriptive title}`

**Rules**:
- Must start with priority bracket: `[P0]`, `[P1]`, `[P2]`, or `[P3]`
- Title must be 10-200 characters (excluding prefix)
- Should be action-oriented and specific
- Use imperative mood ("Add", "Fix", "Implement")

**Examples**:
```
✅ Valid:
  [P0] Consolidate CI/CD Workflows to Eliminate Duplicate Test Runs
  [P1] Update Outdated Dependencies with Security Patches
  [P2] Add Quick Start Section to README
  [P3] Optimize Database Query Performance with Strategic Indexing

❌ Invalid:
  P0 Consolidate CI/CD (missing brackets)
  [P0] CI (too short)
  [P0] This is a really long title that goes on and on and on and exceeds the maximum character limit for titles which is 200 characters and this one is way over that limit making it invalid according to the schema rules (too long)
```

### 3. `priority` Field

**Allowed Values**:
- `critical` (P0) - System-breaking, blocks development
- `high` (P1) - Important features/fixes needed soon
- `medium` (P2) - Improvements and enhancements
- `low` (P3) - Nice-to-have improvements

**Mapping**:
```
P0 → "critical"
P1 → "high"
P2 → "medium"
P3 → "low"
```

**Validation**:
- Must match title prefix (e.g., `[P0]` → `"critical"`)
- Must be lowercase
- Must be one of the four allowed values

### 4. `labels` Field

**Format**: Array of lowercase, kebab-case strings

**Rules**:
- Minimum 1 label (priority label required)
- All labels must be unique
- First label should be priority label
- Pattern: `^[a-z0-9-:/]+$`

**Priority Labels** (required):
- `priority:critical` (P0)
- `priority:high` (P1)
- `priority:medium` (P2)
- `priority:low` (P3)

**Common Category Labels**:
- `ci/cd` - CI/CD related
- `security` - Security issues
- `backend` - Backend changes
- `frontend` - Frontend changes
- `documentation` - Documentation
- `testing` - Test-related
- `dependencies` - Dependency updates
- `developer-experience` - DX improvements
- `infrastructure` - Infrastructure
- `performance` - Performance optimizations
- `monitoring` - Monitoring/observability
- `tech-debt` - Technical debt

**Examples**:
```json
✅ Valid:
["priority:critical", "ci/cd", "tech-debt"]
["priority:high", "security", "backend"]
["priority:medium", "documentation"]
["priority:low", "performance", "database", "optimization"]

❌ Invalid:
[] (empty array)
["high-priority"] (missing priority: prefix)
["Priority:Critical"] (not lowercase)
["ci cd"] (space instead of hyphen)
["priority:critical", "priority:critical"] (duplicates)
```

### 5. `effort_hours` Field

**Format**: Positive number (float or integer)

**Rules**:
- Minimum: 0.25 (15 minutes)
- Maximum: 80 (2 weeks)
- Common increments: 0.25, 0.5, 1, 2, 4, 6, 8, 16, 24, 40, 80

**Typical Ranges by Priority**:
- P0: 1-16 hours (urgent, smaller scope)
- P1: 2-8 hours (important, defined scope)
- P2: 0.25-2 hours (quick improvements)
- P3: 4-8 hours (larger optimizations)

**Examples**:
```json
✅ Valid:
0.25  (15 minutes)
0.5   (30 minutes)
1     (1 hour)
8     (1 day)
16    (2 days)
40    (1 week)

❌ Invalid:
0     (too small)
0.1   (below minimum)
100   (too large - split into smaller issues)
-5    (negative)
```

### 6. `blocks` Field (Optional)

**Format**: Array of strings describing what the issue blocks

**Rules**:
- Optional (typically only used in P0 issues)
- Use kebab-case identifiers
- Be specific but concise

**Examples**:
```json
✅ Valid:
["mvp-features", "session-management", "live-scoring"]
["efficient-development"]
["test-reliability"]
["external-contributions"]

❌ Invalid:
["everything"] (too vague)
["This issue blocks the entire MVP"] (too verbose)
```

### 7. `body` Field

**Format**: Markdown text with required sections

**Minimum Length**: 200 characters

**Required Sections**:
1. `## Problem` - What's wrong or missing
2. `## Impact` OR `## Proposed Solution` - Why it matters or how to fix
3. `## Acceptance Criteria` - Checklist of completion criteria
4. `## Implementation Details` - Reference to detailed specs

**See**: [Body Format Specification](#body-format-specification) for details

---

## Priority Levels

### P0 (Critical) - `priority:critical`

**Definition**: System-breaking issues that block development or pose security risks

**Characteristics**:
- Blocks MVP or core functionality
- Security vulnerabilities
- CI/CD failures blocking team
- Data integrity issues
- Must fix immediately

**Typical Effort**: 1-16 hours (urgent fixes)

**Body Sections**:
- `## Problem` - Critical issue description
- `## Security Risk` OR `## Impact` - Why this is critical
- `## Proposed Solution` - How to fix
- `## Acceptance Criteria` - Definition of done
- `## Implementation Details` - Reference docs

**Label Examples**:
```json
["priority:critical", "security", "backend"]
["priority:critical", "ci/cd", "tech-debt"]
["priority:critical", "testing", "backend"]
```

### P1 (High) - `priority:high`

**Definition**: Important features/fixes needed soon for production readiness

**Characteristics**:
- Important missing features
- Significant security improvements
- Quality/reliability improvements
- Should complete in current sprint

**Typical Effort**: 2-8 hours

**Body Sections**:
- `## Problem` - Issue description
- `## Proposed Solution` - Implementation approach
- `## Acceptance Criteria` - Checklist
- `## Implementation Details` - Reference docs

**Label Examples**:
```json
["priority:high", "security", "dependencies"]
["priority:high", "ci/cd", "frontend", "testing"]
["priority:high", "docker", "developer-experience"]
```

### P2 (Medium) - `priority:medium`

**Definition**: Improvements and enhancements that increase quality

**Characteristics**:
- Documentation improvements
- Developer experience enhancements
- Code quality improvements
- Nice to have, not urgent

**Typical Effort**: 0.25-2 hours (quick wins)

**Body Sections**:
- `## Problem` - What's missing
- `## Proposed Solution` - How to add it
- `## Acceptance Criteria` - Checklist
- `## Implementation Details` - Reference docs

**Label Examples**:
```json
["priority:medium", "documentation", "developer-experience"]
["priority:medium", "code-quality", "developer-experience"]
["priority:medium", "dependencies", "automation"]
```

### P3 (Low) - `priority:low`

**Definition**: Nice-to-have improvements and optimizations

**Characteristics**:
- Performance optimizations
- Additional monitoring/tooling
- Enhanced developer tools
- Future considerations
- Can be deferred indefinitely

**Typical Effort**: 4-8 hours (larger improvements)

**Body Sections**:
- `## Problem` - Opportunity for improvement
- `## Impact` - Benefits of optimization
- `## Proposed Solution` - Implementation approach
- `## Acceptance Criteria` - Success metrics

**Label Examples**:
```json
["priority:low", "performance", "database", "optimization"]
["priority:low", "monitoring", "backend", "observability"]
["priority:low", "documentation", "developer-experience", "nice-to-have"]
```

---

## Body Format Specification

### Standard Template

```markdown
## Problem

[Clear description of what's wrong, missing, or could be improved]
[Use bullet points for multiple aspects]
[Include specific examples or code snippets if relevant]

## Impact OR ## Security Risk OR ## Proposed Solution

[Why this matters / What are the consequences / How to solve it]
[Quantify impact where possible]
[For P0: Include risk assessment]

## Proposed Solution (if not used above)

[How to implement the fix/feature]
[Include code examples, architecture changes, or configuration]
[Break down into steps if complex]

## Acceptance Criteria

- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3
[Minimum 3 criteria, use checkbox format]
[Make each criterion measurable and verifiable]

## Implementation Details

See: `_bmad-output/implementation-artifacts/[reference-doc].md` Section X

**Estimated Effort**: X hours (Y days)  
**Priority**: P0/P1/P2/P3 - [Priority reasoning]  
**Source**: Code Review YYYY-MM-DD
```

### Section Requirements

#### 1. Problem Section

**Required**: ✅ Yes (all priorities)

**Format**:
```markdown
## Problem

[Description of the issue or opportunity]
```

**Guidelines**:
- Start with a clear, concise statement
- Use bullet points for multiple aspects
- Include specific examples or evidence
- Quantify impact where possible
- Keep it factual, not opinionated

**Examples**:

**P0 Example**:
```markdown
## Problem

CI workflows use SQLite for tests while production uses PostgreSQL:

```yaml
# .github/workflows/codacy.yml
DATABASE_URL: sqlite:///./test_trivia.db  # ⚠️ Different from production
```
```

**P2 Example**:
```markdown
## Problem

README is comprehensive but lacks quick start at the top. Users must read extensive documentation before running the application.
```

#### 2. Impact/Risk/Proposed Solution Section

**Required**: ✅ At least one (all priorities)

**Variants**:
- `## Security Risk` - For security issues (typically P0)
- `## Impact` - For issues with measurable consequences
- `## Proposed Solution` - For improvements without negative impact

**Examples**:

**Security Risk (P0)**:
```markdown
## Security Risk

**HIGH**: Without automatic scoping, a developer could accidentally:
- Return data from wrong organization
- Allow cross-tenant data access
- Create compliance violations (GDPR, SOC 2)
```

**Impact (P1)**:
```markdown
## Impact

- **Performance**: Faster queries for user/organization lookups
- **Scalability**: Better handling of larger datasets
```

**Proposed Solution (P2)**:
```markdown
## Proposed Solution

Add quick start section at top of README.md with:
- One-command Docker startup
- Manual setup steps
- Access URLs for frontend, backend, and API docs
```

#### 3. Acceptance Criteria Section

**Required**: ✅ Yes (all priorities)

**Format**:
```markdown
## Acceptance Criteria

- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3
- [ ] Additional criteria as needed
```

**Guidelines**:
- Minimum 3 criteria
- Each criterion must be:
  - **Specific**: No ambiguity
  - **Testable**: Can verify completion
  - **Measurable**: Clear success condition
- Use checkbox format: `- [ ]`
- Write in active voice
- Include both technical and documentation criteria

**Examples**:

**Good**:
```markdown
- [ ] PostgreSQL service added to CI workflows
- [ ] All tests use PostgreSQL in CI
- [ ] Migrations run before tests
- [ ] Test database properly cleaned between runs
- [ ] No SQLite-specific code in tests
```

**Bad**:
```markdown
- [ ] Fix the database issue (not specific)
- [ ] Make it work (not measurable)
- [ ] Tests should pass (not specific enough)
```

#### 4. Implementation Details Section

**Required**: ✅ Yes (all priorities)

**Format**:
```markdown
## Implementation Details

See: `_bmad-output/implementation-artifacts/[filename].md` Section X

**Estimated Effort**: X hours (Y days)  
**Priority**: PX - [Priority reasoning]  
**Source**: [Source of issue]
```

**Guidelines**:
- Reference detailed implementation docs
- Include estimated effort in hours
- Convert to days if > 8 hours: `16 hours (2 days)`
- State priority and reasoning
- Include source/origin

**Examples**:
```markdown
## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 4

**Estimated Effort**: 2 hours  
**Priority**: P0 - Test Reliability  
**Source**: Code Review 2026-02-02
```

### Code Blocks in Body

**Use fenced code blocks** for:
- Configuration examples
- Code snippets
- Command examples
- YAML/JSON structures

**Format**:
````markdown
```yaml
# Example configuration
services:
  postgres:
    image: postgres:13
```

```python
# Example code
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
```

```bash
# Example commands
docker-compose up -d
npm test
```
````

### Markdown Formatting

**Allowed elements**:
- Headers: `##`, `###` (not `#` - reserved for title)
- Bold: `**text**`
- Italic: `*text*`
- Code inline: `` `code` ``
- Code blocks: ` ```lang\ncode\n``` `
- Lists: `- item` or `1. item`
- Checkboxes: `- [ ] item`
- Links: `[text](url)`
- Blockquotes: `> quote`

**Avoid**:
- HTML tags (use Markdown equivalents)
- Images in issue bodies (link instead)
- Tables (can be complex, use lists instead)

---

## Label Format

### Priority Labels (Required)

**Must include exactly one**:

| Priority | Label | Description |
|----------|-------|-------------|
| P0 | `priority:critical` | System-breaking, blocks development |
| P1 | `priority:high` | Important features/fixes |
| P2 | `priority:medium` | Improvements and enhancements |
| P3 | `priority:low` | Nice-to-have optimizations |

### Category Labels (Recommended)

**Technology Stack**:
- `backend` - Backend/API changes
- `frontend` - Frontend/UI changes
- `database` - Database changes
- `infrastructure` - Infrastructure/DevOps

**Functional Areas**:
- `ci/cd` - Continuous Integration/Deployment
- `security` - Security issues/improvements
- `testing` - Test-related
- `documentation` - Documentation changes
- `monitoring` - Monitoring/observability

**Impact/Type**:
- `tech-debt` - Technical debt
- `performance` - Performance improvements
- `developer-experience` - Developer experience
- `automation` - Automation improvements
- `optimization` - Code/system optimizations

**Specific Features**:
- `websocket` - WebSocket functionality
- `real-time` - Real-time features
- `multi-tenancy` - Multi-tenant features
- `dependencies` - Dependency management
- `code-quality` - Code quality

**Nice-to-Have**:
- `nice-to-have` - Optional improvements (P3)

### Label Combinations

**P0 Examples**:
```json
["priority:critical", "ci/cd", "tech-debt"]
["priority:critical", "security", "multi-tenancy", "backend"]
["priority:critical", "testing", "ci/cd", "backend"]
```

**P1 Examples**:
```json
["priority:high", "security", "dependencies", "backend", "frontend"]
["priority:high", "ci/cd", "frontend", "testing"]
["priority:high", "docker", "developer-experience", "infrastructure"]
```

**P2 Examples**:
```json
["priority:medium", "documentation", "developer-experience"]
["priority:medium", "code-quality", "developer-experience"]
["priority:medium", "documentation", "architecture"]
```

**P3 Examples**:
```json
["priority:low", "performance", "database", "optimization"]
["priority:low", "monitoring", "backend", "observability"]
["priority:low", "documentation", "developer-experience", "nice-to-have"]
```

---

## Validation Rules

### Automated Validation

The [`scripts/lib/issue_validator.py`](../../scripts/lib/issue_validator.py) module enforces these rules:

#### 1. Required Field Validation

```python
def validate_issue(issue: Dict) -> Tuple[bool, Optional[str]]:
    """Validate that issue has all required fields"""
    required_fields = ['title', 'body', 'labels', 'priority']
    for field in required_fields:
        if field not in issue:
            return False, f"Missing required field: {field}"
        if not issue[field]:
            return False, f"Empty required field: {field}"
    return True, None
```

#### 2. Priority Validation

```python
def normalize_priority(priority: str) -> str:
    """Normalize priority to standard format"""
    priority_map = {
        'critical': 'critical',
        'high': 'high',
        'medium': 'medium',
        'low': 'low',
        'p0': 'critical',
        'p1': 'high',
        'p2': 'medium',
        'p3': 'low'
    }
    return priority_map.get(priority.lower(), priority.lower())
```

#### 3. Label Validation

```python
def merge_labels(labels: List[str], priority: str) -> List[str]:
    """Merge issue labels with priority labels"""
    priority_labels = get_priority_labels(priority)
    all_labels = list(set(labels + priority_labels))
    return sorted(all_labels)
```

### Manual Validation Checklist

Before creating issues, verify:

- [ ] **JSON structure** is valid (use JSON validator)
- [ ] **All required fields** are present
- [ ] **ID format** matches pattern: `P[0-3]-[0-9]+`
- [ ] **Title format** matches pattern: `[P0-3] ...`
- [ ] **Priority** matches title prefix
- [ ] **Labels** include priority label
- [ ] **Effort hours** is reasonable (0.25-80)
- [ ] **Body** has all required sections
- [ ] **Acceptance criteria** uses checkbox format
- [ ] **Code blocks** use proper fencing
- [ ] **Markdown** is properly formatted
- [ ] **References** point to existing docs

---

## Examples by Priority

### P0 (Critical) - Complete Example

```json
{
  "id": "P0-2",
  "title": "[P0] Implement Organization Scoping Middleware for Multi-Tenancy",
  "priority": "critical",
  "labels": ["priority:critical", "security", "multi-tenancy", "backend"],
  "effort_hours": 8,
  "blocks": ["feature-development", "data-security"],
  "body": "## Problem\n\nMulti-tenant data isolation is not enforced at the application layer. Currently:\n- No middleware to automatically filter by `organization_id`\n- Developers must manually add filters to every query\n- Risk of data leakage between tenants\n\n## Security Risk\n\n**HIGH**: Without automatic scoping, a developer could accidentally:\n- Return data from wrong organization\n- Allow cross-tenant data access\n- Create compliance violations (GDPR, SOC 2)\n\n## Proposed Solution\n\nImplement organization scoping at two levels:\n\n1. **Middleware**: Extract organization from JWT and set in request context\n2. **Base CRUD Class**: Automatically filter all queries by organization_id\n\n```python\n# backend/core/multi_tenancy.py\nasync def get_current_organization(\n    token: str = Depends(oauth2_scheme),\n    db: Session = Depends(get_db)\n) -> Organization:\n    \"\"\"Extract organization from JWT and validate access\"\"\"\n```\n\n## Acceptance Criteria\n\n- [ ] Middleware extracts organization from JWT\n- [ ] Base CRUD class auto-filters by organization_id\n- [ ] All existing CRUD operations use base class\n- [ ] Integration tests validate tenant isolation\n- [ ] Documentation updated with usage examples\n- [ ] No queries bypass organization filter\n\n## Implementation Details\n\nSee: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 2\n\n**Estimated Effort**: 1 day (8 hours)  \n**Priority**: P0 - Security Critical  \n**Source**: Code Review 2026-02-02"
}
```

### P1 (High) - Complete Example

```json
{
  "id": "P1-1",
  "title": "[P1] Update Outdated Dependencies with Security Patches",
  "priority": "high",
  "labels": ["priority:high", "security", "dependencies", "backend", "frontend"],
  "effort_hours": 4,
  "body": "## Problem\n\nMultiple packages have security updates and performance improvements available:\n\n**Backend**:\n- `fastapi`: 0.109.0 → 0.115.0+ (security & performance)\n- `pydantic`: 2.12.5 → 2.13.x (security fixes - CVEs)\n- `pytest`: 7.4.4 → 8.x (better performance)\n\n**Frontend**:\n- `react`: ^18.2.0 → ^18.3.1\n- `vite`: ^5.0.8 → ^5.4.x (security patches)\n\n## Security Impact\n\n- Pydantic 2.12.5 has known security vulnerabilities\n- `python-jose` has CVEs - consider migrating to `PyJWT`\n- Vite has security patches in 5.4.x\n\n## Proposed Solution\n\n1. Update backend dependencies in `requirements.txt`\n2. Update frontend dependencies in `package.json`\n3. Run full test suite after each ecosystem update\n4. Document any breaking changes\n\n## Acceptance Criteria\n\n- [ ] All major dependencies updated to latest stable\n- [ ] Backend tests pass\n- [ ] Frontend tests pass\n- [ ] No new deprecation warnings\n- [ ] CHANGELOG updated with dependency changes\n- [ ] Security scan shows no critical vulnerabilities\n\n## Implementation Details\n\nSee: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 6\n\n**Estimated Effort**: 4 hours (+ testing)  \n**Priority**: P1 - Security & Performance  \n**Source**: Code Review 2026-02-02"
}
```

### P2 (Medium) - Complete Example

```json
{
  "id": "P2-1",
  "title": "[P2] Add Quick Start Section to README",
  "priority": "medium",
  "labels": ["priority:medium", "documentation", "developer-experience"],
  "effort_hours": 0.25,
  "body": "## Problem\n\nREADME is comprehensive but lacks quick start at the top. Users must read extensive documentation before running the application.\n\n## Proposed Solution\n\nAdd quick start section at top of README.md with:\n- One-command Docker startup\n- Manual setup steps\n- Access URLs for frontend, backend, and API docs\n\n## Acceptance Criteria\n\n- [ ] Quick start section added at top of README\n- [ ] Single-command option documented\n- [ ] Manual setup documented\n- [ ] All commands tested and work\n- [ ] Time-to-first-run < 5 minutes for new contributors\n\n## Implementation Details\n\nSee: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 11\n\n**Estimated Effort**: 15 minutes  \n**Priority**: P2 - Documentation  \n**Source**: Code Review 2026-02-02"
}
```

### P3 (Low) - Complete Example

```json
{
  "id": "P3-1",
  "title": "[P3] Optimize Database Query Performance with Strategic Indexing",
  "priority": "low",
  "labels": ["priority:low", "performance", "database", "optimization"],
  "effort_hours": 6,
  "body": "## Problem\n\nCurrent database queries could be optimized with additional strategic indexes on commonly filtered columns.\n\n## Impact\n\n- **Performance**: Faster queries for user/organization lookups\n- **Scalability**: Better handling of larger datasets\n\n## Proposed Solution\n\n- Add indexes on frequently filtered columns: `(organization_id, status)`, `(user_id, created_at)`\n- Profile queries and identify slow operations\n- Document index strategy\n\n## Acceptance Criteria\n\n- [ ] Identify slow queries via EXPLAIN ANALYZE\n- [ ] Create migration for new indexes\n- [ ] Query performance improved by 20%+\n- [ ] Database documentation updated\n\n**Estimated Effort**: 6 hours\n**Priority**: P3 - Nice-to-have optimization\n**Source**: Code Review 2026-02-02"
}
```

---

## Migration Guide

### From Legacy Format to New Format

If you have issues in the old format, use this mapping:

#### Legacy Shell Script Format

**Before** (create-code-review-issues.sh):
```bash
create_issue "[P0] Title" \
"Body text..." \
"label1,label2"
```

**After** (JSON format):
```json
{
  "id": "P0-1",
  "title": "[P0] Title",
  "priority": "critical",
  "labels": ["priority:critical", "label1", "label2"],
  "effort_hours": 3,
  "body": "Body text..."
}
```

#### Legacy Python Dictionary Format

**Before**:
```python
issue = {
    'title': '[P1] Title',
    'body': 'Description',
    'labels': 'label1,label2'
}
```

**After**:
```json
{
  "id": "P1-1",
  "title": "[P1] Title",
  "priority": "high",
  "labels": ["priority:high", "label1", "label2"],
  "effort_hours": 2,
  "body": "Description"
}
```

### Creating New Issues

**Step 1**: Choose priority level (P0-P3)

**Step 2**: Create JSON structure following schema

**Step 3**: Write body following template:
1. Problem section
2. Impact/Risk/Solution section
3. Acceptance criteria (checkboxes)
4. Implementation details

**Step 4**: Validate using schema checker:
```bash
# Using the validation script
python scripts/lib/issue_validator.py <json-file>
```

**Step 5**: Add to appropriate file:
- P0 → `code-review-issues-p0.json`
- P1 → `code-review-issues-p1.json`
- P2 → `code-review-issues-p2.json`
- P3 → `code-review-issues-p3.json`

**Step 6**: Update total_issues count in root object

**Step 7**: Create issues using:
```bash
python scripts/create_issues.py --source json
```

---

## Enforcement

### Automated Enforcement

The following tools enforce this schema:

1. **[`scripts/lib/issue_validator.py`](../../scripts/lib/issue_validator.py)**
   - Validates required fields
   - Normalizes priority values
   - Merges labels correctly

2. **[`scripts/create_issues.py`](../../scripts/create_issues.py)**
   - Validates before creation
   - Rejects invalid issues
   - Reports validation errors

3. **[`scripts/tests/test_lib_modules.py`](../../scripts/tests/test_lib_modules.py)**
   - 37 unit tests
   - Tests all validation logic
   - Ensures schema compliance

### Manual Review

Before committing new issue JSON files:

1. Run JSON validator: `jsonlint <file>.json`
2. Run issue validator: `python scripts/lib/issue_validator.py`
3. Review against checklist in this document
4. Test with dry-run: `python scripts/create_issues.py --dry-run`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-12 | Initial schema based on scripts refactor |

---

## References

- **Source Files**:
  - [`all-issues-to-create.md`](all-issues-to-create.md)
  - [`code-review-issues-p0.json`](code-review-issues-p0.json)
  - [`code-review-issues-p1.json`](code-review-issues-p1.json)
  - [`code-review-issues-p2.json`](code-review-issues-p2.json)
  - [`code-review-issues-p3.json`](code-review-issues-p3.json)

- **Implementation**:
  - [`scripts/lib/issue_validator.py`](../../scripts/lib/issue_validator.py)
  - [`scripts/create_issues.py`](../../scripts/create_issues.py)
  - [`scripts/IMPLEMENTATION_SUMMARY.md`](../../scripts/IMPLEMENTATION_SUMMARY.md)

- **Related Documentation**:
  - [`scripts/README.md`](../../scripts/README.md)
  - [Scripts Refactoring Plan](../../plans/scripts-refactoring-plan.md)

---

**Maintained By**: Development Team  
**Last Updated**: 2026-02-12  
**Schema Version**: 1.0
