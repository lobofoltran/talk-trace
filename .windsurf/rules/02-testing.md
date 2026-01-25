---
trigger: always_on
---

# Testing Rules

- Every public function in service.py / adapters.py MUST have at least 1 unit test
- Mock all external calls (whisper, filesystem writes, HTTP calls to other services)
- Use pytest fixtures for session_id and temp paths
- Aim for 85–95% coverage per file
- Run coverage after every major change