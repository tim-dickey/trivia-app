# Testing Report - 2026-02-07

**Project**: trivia-app  
**Scope**: Backend test suite  
**Command**: `cd backend && python -m pytest`  
**Environment**: Windows (local), venv Python 3.13.12

## Result

**Status**: PASSED

```
130 passed, 4 skipped, 399 warnings in 25.67s
```

## Notes

- Test run used `venv` at `C:\Users\tdick\OneDrive\Documents\GitHub\trivia-app\venv`.
- SQLite-backed tests ran; PostgreSQL-specific checks were skipped (4 skipped).
- Coverage: 96.29% (threshold 80% met).

### Warnings Observed

- Starlette `python-multipart` import deprecation
- SQLAlchemy `declarative_base()` deprecation (2.0)
- Pydantic class-based config deprecation (V2)
- httpx `app` shortcut deprecation
- `datetime.utcnow()` deprecation warnings (core + tests)

## Next Steps

1. Consider updating deprecated usage paths when planning future refactors.
