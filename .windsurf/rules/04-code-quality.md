---
trigger: always_on
---

# Code Quality Rules – TalkTrace

## Clean Architecture Requirements
- **Python files MUST NEVER exceed 200 lines** (except __init__.py and long test files)
- **Functions should be max ~30–40 lines** (ideal < 20)
- **Test coverage > 80% per service** (measured by coverage.py)
- **Use Ruff exclusively for formatting/linting**
- **Type hints mandatory for public functions and classes**
- **Google-style docstrings for all public functions/methods**
- **Avoid any global state** (except config via env vars)
- **Prefer dependency injection** (pass fs adapter, http client, etc)
- **Follow Clean Architecture layering** - never import from outer layers
- **Interface segregation** - keep interfaces small and focused

## Clean Architecture Specific Rules
- **Domain layer**: Pure business logic, no external dependencies
- **Application layer**: Use cases, orchestrates domain and infrastructure
- **Infrastructure layer**: External integrations, implements domain interfaces
- **API layer**: HTTP endpoints, request/response mapping only
- **Dependency direction**: Inward only (Domain ← Application ← Infrastructure ← API)

When proposing code:
- Always include corresponding tests in the same response if possible
- Suggest commit message in Conventional Commits format
- Indicate which branch the work should be done on
- Ensure Clean Architecture compliance in all changes