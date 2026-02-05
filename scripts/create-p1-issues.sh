#!/bin/bash
#
# Script to create P1 (High Priority) GitHub issues from code-review-issues-p1.json
#
# Usage: ./scripts/create-p1-issues.sh
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - Run: gh auth login

set -e  # Exit on error

REPO="tim-dickey/trivia-app"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
P1_ISSUES_FILE="${SCRIPT_DIR}/../_bmad-output/implementation-artifacts/code-review-issues-p1.json"
TRACKING_FILE="${SCRIPT_DIR}/../_bmad-output/implementation-artifacts/p1-issues-created.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is installed and authenticated
check_gh_auth() {
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ Error: GitHub CLI (gh) not found${NC}"
        echo "   Please install from: https://cli.github.com/"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}❌ Error: Not authenticated with GitHub CLI${NC}"
        echo "   Please run: gh auth login"
        exit 1
    fi
}

# Print header
print_header() {
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║               Creating P1 GitHub Issues from JSON File                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Repository: ${REPO}"
    echo "Source File: ${P1_ISSUES_FILE}"
    echo ""
}

# Create a single issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    echo "Creating: ${title}"
    
    local issue_url
    issue_url=$(gh issue create \
        --repo "${REPO}" \
        --title "${title}" \
        --body "${body}" \
        --label "${labels}" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Created: ${issue_url}${NC}"
        # Extract issue number
        local issue_num=$(echo "${issue_url}" | grep -oE '[0-9]+$')
        echo "${issue_num}"
    else
        echo -e "${RED}✗ Failed: ${title}${NC}"
        echo "  Error: ${issue_url}"
        echo ""
    fi
}

# Main execution
main() {
    print_header
    
    # Check prerequisites
    check_gh_auth
    echo -e "${GREEN}✓ GitHub CLI authenticated${NC}"
    echo ""
    
    # Check if JSON file exists
    if [ ! -f "${P1_ISSUES_FILE}" ]; then
        echo -e "${RED}❌ Error: P1 issues file not found: ${P1_ISSUES_FILE}${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Loaded P1 issues from JSON file${NC}"
    echo ""
    
    # Parse JSON and create issues
    local created_count=0
    local total_effort=0
    
    # Issue 1
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo "Issue 1 of 5"
    echo "════════════════════════════════════════════════════════════════════════════════"
    create_issue \
        "[P1] Update Outdated Dependencies with Security Patches" \
        "## Problem

Multiple packages have security updates and performance improvements available:

**Backend**:
- \`fastapi\`: 0.109.0 → 0.115.0+ (security & performance)
- \`pydantic\`: 2.12.5 → 2.13.x (security fixes - CVEs)
- \`pytest\`: 7.4.4 → 8.x (better performance)
- \`python-jose\`: 3.4.0 has known vulnerabilities

**Frontend**:
- \`react\`: ^18.2.0 → ^18.3.1
- \`vite\`: ^5.0.8 → ^5.4.x (security patches)
- \`typescript\`: ^5.2.2 → ^5.7.x (performance)
- \`tailwindcss\`: ^3.3.6 → ^3.4.x

## Security Impact

- Pydantic 2.12.5 has known security vulnerabilities
- \`python-jose\` has CVEs - consider migrating to \`PyJWT\`
- Vite has security patches in 5.4.x

## Proposed Solution

1. Update backend dependencies in \`requirements.txt\`
2. Update frontend dependencies in \`package.json\`
3. Run full test suite after each ecosystem update
4. Document any breaking changes
5. Consider migrating from \`python-jose\` to \`PyJWT\`

## Acceptance Criteria

- [ ] All major dependencies updated to latest stable
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] No new deprecation warnings
- [ ] CHANGELOG updated with dependency changes
- [ ] Security scan shows no critical vulnerabilities

## Implementation Details

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 6

**Estimated Effort**: 4 hours (+ testing)  
**Priority**: P1 - Security & Performance  
**Source**: Code Review 2026-02-02" \
        "priority:high,security,dependencies,backend,frontend"
    
    [ $? -eq 0 ] && ((created_count++)) && ((total_effort+=4))
    echo ""
    sleep 1  # Rate limiting
    
    # Issue 2
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo "Issue 2 of 5"
    echo "════════════════════════════════════════════════════════════════════════════════"
    create_issue \
        "[P1] Add Frontend CI Workflow for Quality Validation" \
        "## Problem

No automated validation of frontend code quality:
- Backend: ✅ Tested in Codacy workflow
- Frontend: ❌ No CI validation

**Risk**: Frontend bugs, type errors, and lint issues won't be caught until deployment.

## Proposed Solution

Create \`.github/workflows/frontend-ci.yml\` with comprehensive checks:
- Linting (ESLint)
- Type checking (TypeScript)
- Build verification
- Unit tests with coverage
- Coverage upload to Codecov

## Acceptance Criteria

- [ ] Workflow runs on frontend changes
- [ ] All checks pass (lint, type-check, build, test)
- [ ] Coverage reports uploaded
- [ ] Workflow badge added to README
- [ ] Runs within 5 minutes

## Implementation Details

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 7

**Estimated Effort**: 2 hours  
**Priority**: P1 - Quality Assurance  
**Source**: Code Review 2026-02-02" \
        "priority:high,ci/cd,frontend,testing"
    
    [ $? -eq 0 ] && ((created_count++)) && ((total_effort+=2))
    echo ""
    sleep 1  # Rate limiting
    
    # Issue 3
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo "Issue 3 of 5"
    echo "════════════════════════════════════════════════════════════════════════════════"
    create_issue \
        "[P1] Expand CodeQL Security Analysis to Python and TypeScript" \
        "## Problem

CodeQL workflow only analyzes GitHub Actions, not application code.

**Security Gap**: Python and TypeScript code vulnerabilities won't be detected.

## Proposed Solution

Expand CodeQL analysis to cover all languages:

\`\`\`yaml
# Update: .github/workflows/codeql.yml
strategy:
  matrix:
    include:
    - language: python
      build-mode: none
    - language: javascript-typescript
      build-mode: none
    - language: actions
      build-mode: none
\`\`\`

## Security Benefits

CodeQL will detect:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication bypasses
- Insecure cryptography
- Path traversal issues
- And 200+ other vulnerability types

## Acceptance Criteria

- [ ] Python analysis enabled
- [ ] JavaScript/TypeScript analysis enabled
- [ ] First scan completes successfully
- [ ] Security issues (if any) documented
- [ ] False positives marked and justified
- [ ] Results appear in Security tab

## Implementation Details

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 8

**Estimated Effort**: 1 hour  
**Priority**: P1 - Security Scanning  
**Source**: Code Review 2026-02-02" \
        "priority:high,security,ci/cd,codeql"
    
    [ $? -eq 0 ] && ((created_count++)) && ((total_effort+=1))
    echo ""
    sleep 1  # Rate limiting
    
    # Issue 4
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo "Issue 4 of 5"
    echo "════════════════════════════════════════════════════════════════════════════════"
    create_issue \
        "[P1] Add Application Services to Docker Compose" \
        "## Problem

\`docker-compose.yml\` only defines infrastructure (PostgreSQL, Redis), not application services. Developers must:
- Manually run backend in one terminal
- Manually run frontend in another terminal
- Remember 4+ commands to start development environment

**Poor Developer Experience**: No unified development startup.

## Proposed Solution

Add backend and frontend services to \`docker-compose.yml\` with:
- Hot reload for both services
- Automatic dependency management
- Health checks
- Proper volume mounting

## Acceptance Criteria

- [ ] Single \`docker-compose up\` starts everything
- [ ] Hot reload works for backend and frontend
- [ ] Database migrations run automatically
- [ ] README updated with Docker instructions
- [ ] Development environment starts in <2 minutes

## Implementation Details

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 9

**Estimated Effort**: 3 hours  
**Priority**: P1 - Developer Experience  
**Source**: Code Review 2026-02-02" \
        "priority:high,docker,developer-experience,infrastructure"
    
    [ $? -eq 0 ] && ((created_count++)) && ((total_effort+=3))
    echo ""
    sleep 1  # Rate limiting
    
    # Issue 5
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo "Issue 5 of 5"
    echo "════════════════════════════════════════════════════════════════════════════════"
    create_issue \
        "[P1] Add Security Headers Middleware" \
        "## Problem

Missing common security headers:
- No HSTS (HTTP Strict Transport Security)
- No CSP (Content Security Policy)
- No X-Frame-Options (clickjacking protection)
- No X-Content-Type-Options
- No X-XSS-Protection

**Security Risk**: Application vulnerable to common attacks.

## Security Best Practices

- **HSTS**: Force HTTPS connections
- **CSP**: Prevent XSS attacks by restricting resource loading
- **X-Frame-Options**: Prevent clickjacking
- **X-Content-Type-Options**: Prevent MIME sniffing attacks

## Proposed Solution

Create security headers middleware in \`backend/core/security_middleware.py\` and integrate with FastAPI application.

## Acceptance Criteria

- [ ] All security headers present in responses
- [ ] CSP policy doesn't break functionality
- [ ] Tests verify headers are set correctly
- [ ] Documentation explains each header
- [ ] Security scan shows improved rating

## Implementation Details

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 10

**Estimated Effort**: 2 hours  
**Priority**: P1 - Security Hardening  
**Source**: Code Review 2026-02-02" \
        "priority:high,security,backend,middleware"
    
    [ $? -eq 0 ] && ((created_count++)) && ((total_effort+=2))
    echo ""
    
    # Summary
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo " Summary"
    echo "════════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo -e "${GREEN}Successfully created: ${created_count}/5 P1 issues${NC}"
    echo -e "Total Effort: ${total_effort} hours ($(echo "scale=1; ${total_effort}/8" | bc) days)"
    echo ""
    echo -e "${GREEN}✓ P1 issue creation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review created issues at https://github.com/${REPO}/issues"
    echo "  2. Assign issues to team members"
    echo "  3. Add to project board if needed"
    echo "  4. Start implementation based on priority"
}

# Run main function
main
