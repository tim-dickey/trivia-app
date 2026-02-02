# File Locations Guide - Trivia App

> **Quick Reference**: Where to find files in the trivia-app repository

This guide helps you quickly locate files in the repository. Use `Ctrl+F` / `Cmd+F` to search for specific file types or purposes.

---

## 📚 Documentation Files

### Main Documentation (Root Level)
| File | Location | Purpose |
|------|----------|---------|
| README | `README.md` | Main project documentation, setup instructions |
| Contributing Guide | `CONTRIBUTING.md` | How to contribute, coding standards, PR process |
| License | `LICENSE` | MIT License terms |
| Virtual Environment Guide | `VENV_SETUP.md` | Python virtual environment setup instructions |
| Environment Example | `.env.example` | Template for environment variables |

### docs/ Directory
| File | Location | Purpose |
|------|----------|---------|
| CI/CD Guide | `docs/CI_CD.md` | Comprehensive CI/CD workflows documentation |
| Quick Reference | `docs/QUICK_REFERENCE.md` | Quick command reference |
| Diagrams | `docs/DIAGRAMS.md` | Architecture diagrams and visual aids |
| Epic 1 Validation | `docs/validation/epic-1-validation-report.md` | Epic 1 quality validation |
| Epic 1 Testing | `docs/validation/epic-1-testing-report.md` | Epic 1 test coverage report |

### Implementation Artifacts (_bmad-output/implementation-artifacts/)
| File | Location | Purpose |
|------|----------|---------|
| Architecture | `_bmad-output/implementation-artifacts/architecture.md` | Complete architecture decisions |
| PRD | `_bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md` | Product Requirements Document |
| UI/UX Specs | `_bmad-output/implementation-artifacts/UI_UX_SPECIFICATIONS.md` | User interface specifications |
| QA Strategy | `_bmad-output/implementation-artifacts/QA_TEST_STRATEGY.md` | Testing strategy document |
| Action Items | `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` | Prioritized action items from code review |
| Code Review | `_bmad-output/implementation-artifacts/code-review-2026-02-02.md` | Detailed code review findings |
| Dev Record | `_bmad-output/implementation-artifacts/dev-agent-record.md` | Development implementation record |
| Documentation Summary | `_bmad-output/implementation-artifacts/documentation-update-summary-2026-02-02.md` | Recent documentation updates summary |

### Planning Artifacts (_bmad-output/planning-artifacts/)
| File | Location | Purpose |
|------|----------|---------|
| Epics | `_bmad-output/planning-artifacts/epics.md` | Complete epic breakdown and stories |

### Sprint Tracking (_bmad-output/implementation-artifacts/)
| File | Location | Purpose |
|------|----------|---------|
| Sprint Status | `_bmad-output/implementation-artifacts/sprint-status.yaml` | Current sprint status tracking |

---

## 🔧 Configuration Files

### Root Configuration
| File | Location | Purpose |
|------|----------|---------|
| Docker Compose | `docker-compose.yml` | PostgreSQL and Redis services |
| Git Ignore | `.gitignore` | Git ignored files/directories |
| Codacy Config | `.codacy.yml` | Code quality configuration |
| Pyright Config | `pyrightconfig.json` | Python type checking configuration |

### Backend Configuration (backend/)
| File | Location | Purpose |
|------|----------|---------|
| Requirements | `backend/requirements.txt` | Python dependencies |
| Pytest Config | `backend/pytest.ini` | Test configuration |
| Alembic Config | `backend/alembic.ini` | Database migration configuration |

### Frontend Configuration (frontend/)
| File | Location | Purpose |
|------|----------|---------|
| Package JSON | `frontend/package.json` | Node.js dependencies and scripts |

---

## 💻 Backend Source Code

### Backend Root (backend/)
| File | Location | Purpose |
|------|----------|---------|
| Main Entry | `backend/main.py` | FastAPI application entry point |
| Init | `backend/__init__.py` | Backend package initialization |

### Core Module (backend/core/)
| File | Location | Purpose |
|------|----------|---------|
| Configuration | `backend/core/config.py` | Pydantic settings and environment config |
| Database | `backend/core/database.py` | SQLAlchemy engine and session management |
| Security | `backend/core/security.py` | JWT tokens, password hashing (bcrypt) |

### Models (backend/models/)
| File | Location | Purpose |
|------|----------|---------|
| User Model | `backend/models/user.py` | User ORM model with organization FK |
| Organization Model | `backend/models/organization.py` | Organization ORM model |

### Schemas (backend/schemas/)
| File | Location | Purpose |
|------|----------|---------|
| Auth Schemas | `backend/schemas/auth.py` | Login, token, JWT payload schemas |
| User Schemas | `backend/schemas/user.py` | User request/response schemas |
| Organization Schemas | `backend/schemas/organization.py` | Organization request/response schemas |

### API Endpoints (backend/api/)
| Directory | Location | Purpose |
|-----------|----------|---------|
| V1 Endpoints | `backend/api/v1/endpoints/` | API version 1 endpoints |
| Auth Endpoints | `backend/api/v1/endpoints/auth.py` | Registration, login, logout endpoints |

### Database CRUD (backend/db/)
| Directory | Location | Purpose |
|-----------|----------|---------|
| CRUD Operations | `backend/db/crud/` | Database CRUD functions |
| User CRUD | `backend/db/crud/user_crud.py` | User database operations |
| Organization CRUD | `backend/db/crud/organization_crud.py` | Organization database operations |

### Other Backend Modules
| Directory | Location | Purpose |
|-----------|----------|---------|
| Services | `backend/services/` | Business logic layer (empty structure) |
| WebSocket | `backend/websocket/` | WebSocket handlers (empty structure) |
| Integrations | `backend/integrations/` | External API integrations (empty structure) |
| Tasks | `backend/tasks/` | Background tasks (empty structure) |

### Database Migrations (backend/alembic/)
| Directory | Location | Purpose |
|-----------|----------|---------|
| Alembic Env | `backend/alembic/env.py` | Alembic environment configuration |
| Migrations | `backend/alembic/versions/` | Database migration scripts |

---

## 🧪 Backend Tests

### Test Structure (backend/tests/)
| Directory/File | Location | Purpose |
|----------------|----------|---------|
| Test Config | `backend/tests/conftest.py` | Pytest fixtures and test configuration |
| Model Tests | `backend/tests/models/` | ORM model tests |
| User Model Tests | `backend/tests/models/test_user.py` | User model tests |
| Organization Tests | `backend/tests/models/test_organization.py` | Organization model tests |
| CRUD Tests | `backend/tests/crud/` | Database CRUD operation tests |
| User CRUD Tests | `backend/tests/crud/test_user_crud.py` | User CRUD tests |
| Org CRUD Tests | `backend/tests/crud/test_organization_crud.py` | Organization CRUD tests |
| API Tests | `backend/tests/api/` | API endpoint integration tests |
| Auth API Tests | `backend/tests/api/test_auth.py` | Authentication endpoint tests |

**Running Tests**:
```bash
# From project root
pytest backend/tests --cov=backend

# From backend directory
cd backend && PYTHONPATH=.. pytest
```

---

## 🎨 Frontend Source Code

### Frontend Structure (frontend/)
| Directory | Location | Purpose | Status |
|-----------|----------|---------|--------|
| Components | `frontend/src/components/` | React components | ⏳ Placeholder |
| Hooks | `frontend/src/hooks/` | Custom React hooks | ⏳ Placeholder |
| Store | `frontend/src/store/` | Zustand state management | ⏳ Placeholder |
| Services | `frontend/src/services/` | API service functions | ⏳ Placeholder |
| Pages | `frontend/src/pages/` | Page components | ⏳ Placeholder |
| Types | `frontend/src/types/` | TypeScript type definitions | ⏳ Placeholder |
| Styles | `frontend/src/styles/` | CSS/styling files | ⏳ Placeholder |

**Note**: Frontend implementation is planned but not yet developed. Directory structure exists with `.gitkeep` files.

---

## 🔄 CI/CD Workflows

### GitHub Actions (.github/workflows/)
| File | Location | Purpose | Triggers |
|------|----------|---------|----------|
| Codacy | `.github/workflows/codacy.yml` | Code quality, coverage, security | PRs, main, weekly |
| CodeQL | `.github/workflows/codeql.yml` | Security vulnerability scanning | PRs, main, weekly |
| Greetings | `.github/workflows/greetings.yml` | Welcome new contributors | First issue/PR |
| Summary | `.github/workflows/summary.yml` | AI issue summarization | New issues |
| Dependency Review | `.github/workflows/dependency-review.yml.disabled` | Dependency scanning | Disabled |

### GitHub Configuration (.github/)
| File | Location | Purpose |
|------|----------|---------|
| Copilot Instructions | `.github/copilot-instructions.md` | AI assistant context and guidelines |
| Codacy Instructions | `.github/instructions/codacy.instructions.md` | Codacy-specific rules |
| Labeler Config | `.github/labeler.yml` | Auto-labeling configuration |

### Custom Agents (.github/agents/)
23 custom agent definitions for BMAD framework:
- Core: `bmd-custom-core-bmad-master.agent.md`
- BMM: `bmd-custom-bmm-*.agent.md` (analyst, architect, dev, pm, sm, tea, tech-writer, ux-designer, quick-flow-solo-dev)
- BMB: `bmd-custom-bmb-*.agent.md` (agent-builder, module-builder, workflow-builder)
- CIS: `bmd-custom-cis-*.agent.md` (brainstorming-coach, creative-problem-solver, design-thinking-coach, innovation-strategist, presentation-master, storyteller)

---

## 🛠️ Scripts

### Utility Scripts (scripts/)
| File | Location | Purpose |
|------|----------|---------|
| Issue Creation | `scripts/create-github-issues.py` | Python script to create GitHub issues |
| Code Review Issues | `scripts/create-code-review-issues.sh` | Bash script for code review issue creation |
| Issue Runner | `scripts/run-issue-creation.sh` | Wrapper script for issue creation |

---

## 📁 Special Directories

### BMAD Framework (_bmad/)
Configuration and workflow definitions for the BMAD agent framework:
- `_bmad/_config/` - Agent configurations
- `_bmad/bmb/` - Module builder workflows
- `_bmad/bmm/` - Methodology management
- `_bmad/cis/` - Creative innovation support
- `_bmad/core/` - Core framework files

### Build Artifacts (Generated, Not Committed)
| Directory | Purpose | Location |
|-----------|---------|----------|
| Python Virtual Env | Virtual environment | `backend/venv/` |
| Node Modules | NPM packages | `frontend/node_modules/` |
| Coverage Reports | Test coverage HTML | `backend/htmlcov/` |
| Python Cache | Compiled Python | `**/__pycache__/`, `**/*.pyc` |
| Pytest Cache | Test cache | `**/.pytest_cache/` |

---

## 🔍 Quick Find Reference

### "I need to..."

**Add a new API endpoint:**
1. Define schemas in `backend/schemas/`
2. Create/update models in `backend/models/`
3. Create migration: `cd backend && alembic revision --autogenerate -m "description"`
4. Add CRUD in `backend/db/crud/`
5. Add endpoint in `backend/api/v1/endpoints/`
6. Write tests in `backend/tests/api/`

**Run the application:**
```bash
# Start infrastructure
docker-compose up -d

# Backend
cd backend && python main.py
# Runs at http://localhost:8000
# API docs at http://localhost:8000/docs

# Frontend (when implemented)
cd frontend && npm run dev
# Runs at http://localhost:5173
```

**Run tests:**
```bash
# Backend
cd backend && PYTHONPATH=.. pytest --cov=backend

# Frontend (when implemented)
cd frontend && npm test
```

**Check CI/CD workflows:**
- See detailed guide: `docs/CI_CD.md`
- View workflow files: `.github/workflows/`

**Find documentation:**
- Setup: `README.md`
- Contributing: `CONTRIBUTING.md`
- Architecture: `_bmad-output/implementation-artifacts/architecture.md`
- CI/CD: `docs/CI_CD.md`

**Create database migration:**
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Format and lint code:**
```bash
# Backend
cd backend
black .
ruff check .

# Frontend (when implemented)
cd frontend
npm run lint
```

---

## 📊 File Statistics

**Total Structure**:
- Backend Python files: ~30 source files, ~20 test files
- Documentation: 40+ markdown files
- Configuration: 10+ config files
- CI/CD Workflows: 5 active workflows
- Custom Agents: 23 agent definitions

**Documentation Coverage**:
- ✅ Architecture decisions documented
- ✅ API endpoints documented (in code + Swagger)
- ✅ CI/CD workflows documented
- ✅ Setup and contribution guides complete
- ✅ Testing strategy documented
- ⏳ Frontend documentation pending (not implemented)

---

## 🔗 Related Documentation

- **Setup Instructions**: See `README.md` → Setup Instructions
- **Contributing**: See `CONTRIBUTING.md` → Development Workflow
- **Architecture Decisions**: See `_bmad-output/implementation-artifacts/architecture.md`
- **Sprint Status**: See `_bmad-output/implementation-artifacts/sprint-status.yaml`
- **CI/CD Details**: See `docs/CI_CD.md`
- **Action Items**: See `_bmad-output/implementation-artifacts/action-items-2026-02-02.md`

---

## 💡 Tips

1. **Use IDE Search**: Most IDEs support "Go to File" (Ctrl+P / Cmd+P)
2. **Use grep**: `grep -r "function_name" backend/`
3. **Use find**: `find . -name "*.py" -path "*/tests/*"`
4. **Check imports**: Follow import statements to locate modules
5. **API Documentation**: Run backend and visit http://localhost:8000/docs

---

**Last Updated**: February 2, 2026  
**Maintained By**: Development Team  
**Questions?**: See `CONTRIBUTING.md` or open an issue
