---
trigger: always_on
---

# Simulate PR Review Checklist (use when finishing a task)

Before marking a task as complete, mentally run this checklist:

1. File length ≤ 200 lines per file?
2. Coverage still >80%? (remind to run coverage)
3. Conventional Commit message ready?
4. Docstrings/type hints added where public?
5. Artifacts written + errors.log handled?
6. Determinism preserved (no new random/timestamp sources)?
7. Mocks used in tests for externals?
8. Happy path + 2–3 error cases tested?
9. Dependencies injected (no hardcoded paths)?
10. Follows existing naming/patterns in the service?

If any no → fix before proposing merge/PR