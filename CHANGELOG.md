# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

#### Backend
- **CRITICAL**: Migrated from `python-jose` to `PyJWT` (2.10.1) to address CVE vulnerabilities
- **CRITICAL**: Updated `fastapi` from 0.109.0 to 0.115.6 (fixes ReDoS vulnerability in Content-Type header parsing)
- Updated `cryptography` to 44.0.0 for PyJWT cryptographic algorithms support
- Updated `uvicorn` from 0.27.0 to 0.34.0 (includes security patches)
- Updated `pydantic-settings` from 2.1.0 to 2.12.0
- Updated `email-validator` from 2.1.0 to 2.2.0

#### Frontend
- **CRITICAL**: Updated `vite` from 5.0.8 to 5.4.21 (fixes file system bypass vulnerability)
- Updated `react` and `react-dom` from 18.2.0 to 18.3.1
- Updated `typescript` from 5.2.2 to 5.7.3 (performance improvements)
- Updated `tailwindcss` from 3.3.6 to 3.4.19

### Changed

#### Backend
- Replaced `python-jose[cryptography]` with separate `PyJWT` and `cryptography` packages
- Updated import statement in `backend/core/security.py`:
  - Changed: `from jose import jwt, JWTError`
  - To: `import jwt` and `from jwt.exceptions import PyJWTError`
- Updated exception handling in token decoding to use `PyJWTError` instead of `JWTError`

### Testing
- All backend tests pass (133/134 tests, 96% coverage maintained)
- Frontend builds successfully with updated dependencies
- No breaking changes in API contracts

### Notes
- `pytest` was already at version 9.0.2 (newer than target 8.x)
- `pydantic` remains at 2.12.5 (latest stable version in 2.x series at time of update)
- Security scan shows no critical vulnerabilities after updates

### Deprecation Warnings
The following deprecation warnings were identified but not yet addressed:
- Pydantic V2: Class-based `config` is deprecated (use `ConfigDict` instead)
- SQLAlchemy 2.0: `declarative_base()` moved to `sqlalchemy.orm.declarative_base()`
- Python: `datetime.utcnow()` is deprecated (use `datetime.now(datetime.UTC)` instead)
- These warnings will be addressed in a future update

## [0.1.0] - 2026-02-02

### Added
- Initial backend implementation with FastAPI
- User authentication with JWT tokens
- Multi-tenant organization support
- PostgreSQL database with Alembic migrations
- Comprehensive test suite
- CI/CD workflows
