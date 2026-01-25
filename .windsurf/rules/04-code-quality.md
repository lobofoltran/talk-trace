---
trigger: always_on
---

# Code Quality Rules – TalkTrace

- Python files MUST NEVER exceed 200 lines (except __init__.py and long test files)
- Functions should be max ~30–40 lines (ideal < 20)
- Test coverage > 80% per service (measured by coverage.py)
- Use black + isort + flake8 (or ruff) for formatting/linting
- Type hints mandatory for public functions and classes
- Google-style docstrings for all public functions/methods
- Avoid any global state (except config via env vars)
- Prefer dependency injection (pass fs adapter, http client, etc)

When proposing code:
- Always include corresponding tests in the same response if possible
- Suggest commit message in Conventional Commits format
- Indicate which branch the work should be done on