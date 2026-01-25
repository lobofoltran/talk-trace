---
trigger: always_on
---

# Security & Engineering Best Practices

Security mandates:
- Validate all inputs (file size < 50MB, content-type audio/*, session_id is uuid-like)
- Sanitize filenames before saving (avoid path traversal)
- Never execute code from user input
- Use secure temp dirs for processing (if needed)
- Log sensitive data? NEVER (no tokens, no full audio paths in stdout)

General best practices:
- Follow SOLID where it doesn't add complexity (single responsibility in service.py)
- Prefer pure functions in service.py when possible
- Rate limiting? Add later via middleware if public-facing
- Dependency management: pin versions in requirements.txt; review Dependabot alerts
- When adding deps: justify in commit (e.g. "chore(deps): add pydub for audio preprocessing – needed for format conversion")

Error handling pattern (enforce this):
try:
    result = do_work()
    write_artifact(result)
except Exception as e:
    append_to_errors_log(session_id, str(e), traceback.format_exc())
    raise  # or return error response