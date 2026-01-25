---
trigger: always_on
---

# Git Flow & Commit Enforcement

Current branch rules reminder:
- You are ALWAYS working on a feature/bugfix/... branch, never main/develop directly
- Suggest branch name if user didn't specify (e.g. feature/add-whisper-timestamp-normalization)
- Every response that includes code changes MUST end with:
  - Suggested commit message (Conventional Commits)
  - Suggested branch name
  - PR title/body template if large

Example ending:
Suggested commit: feat(transcriber): add audio duration check and rejection

Suggested branch: feature/transcriber-duration-validation

PR title: feat: add audio duration validation in transcriber