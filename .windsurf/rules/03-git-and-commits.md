---
trigger: always_on
---

# Git and Commit Rules – TalkTrace

## Branch Naming (Git Flow – adapted)

- main                  → production branch (protected, only merges from release/hotfix)
- develop               → integration branch (where all features are merged)
- feature/short-name    → new features (e.g., feature/transcriber-whisper-v3)
- bugfix/ticket-number  → bug fixes (e.g., bugfix/47-transcriber-crash-large-file)
- release/vX.Y.Z        → release preparation (e.g., release/v0.1.0)
- hotfix/ticket-number  → urgent production fixes (e.g., hotfix/89-analyzer-oom)

Mandatory rules:
- NEVER commit directly to main or develop
- Always create branches from develop (except hotfix, which branches from main)
- Branch names in lowercase, kebab-case, max 50 characters
- Required prefixes: feature/, bugfix/, release/, hotfix/

## Conventional Commits (mandatory)

Format:
<type>(<scope>): <short description>

Allowed types:
- feat:     new feature
- fix:      bug fix
- docs:     documentation changes
- style:    formatting, semicolons, etc (no logic change)
- refactor: code refactoring (no feature or bug fix)
- test:     adding or correcting tests
- chore:    maintenance tasks (deps, CI, etc)
- perf:     performance improvements
- ci:       CI/CD pipeline changes
- revert:   revert previous commit

Examples:
feat(transcriber): add support for whisper large-v3 model
fix(analyzer): handle empty transcript gracefully
test(exporter): add integration test for anki card generation
chore(deps): bump flask from 3.0.2 to 3.0.3
docs(readme): update docker-compose usage instructions

Rules:
- First line ≤ 72 characters
- Optional body (detailed explanation)
- Optional footer (e.g., BREAKING CHANGE, Closes #123)
- Use imperative mood (add, fix, update, remove…)
- Scope in parentheses: service or component (transcriber, analyzer, exporter, runtime, tests, docker, etc)

When generating commits, Windsurf must follow this format exactly.