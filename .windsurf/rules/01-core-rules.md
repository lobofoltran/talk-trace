---
trigger: always_on
---

# Core Rules for TalkTrace

- MAX_FILE_LENGTH: 200 lines (hard limit — split if longer)
- MIN_COVERAGE: 80%
- ARTIFACTS_MANDATORY: true
- ERRORS_LOG_APPEND: always
- NO_RANDOM_IN_PIPELINE: true
- SERVICES: transcriber, analyzer, exporter
- COMMUNICATION: HTTP + disk only

When suggesting code:
- Always show imports first
- Keep functions small (< 30 lines ideal)
- Add docstrings to public functions