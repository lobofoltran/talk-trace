---
trigger: always_on
---

# Linting & Formatting Rules – TalkTrace

- Use **Ruff** exclusively for linting and formatting.
- Configuration lives in pyproject.toml at root.
- Always run `ruff check --fix . && ruff format .` before committing.
- In CI: enforce `ruff check --output-format=github` (fail on issues).
- Never introduce new ignores without justification in commit message.
- Prefer Ruff autofix over manual changes when possible.
- Keep files ≤ 200 lines → Ruff will warn on complexity indirectly.
- Type hints: Ruff checks basic annotations (ANN); aim for full coverage in public APIs.

When suggesting code:
- Ensure it would pass `ruff check` with current config.
- If adding new rule violation, explain why and propose ignore + comment.