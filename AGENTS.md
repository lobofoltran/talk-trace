# AGENTS.md — TalkTrace Agent Contract (Codex-First)

**Local-first, artifact-driven speech learning pipeline**

Record → Transcribe → Analyze → Report → Export → Review

This repository is designed to be operated by AI agents (Codex, GPT, Claude) with strict architectural discipline.

---

# 1. NON-NEGOTIABLE RULES (MUST)

## 1.1 Minimal + Pragmatic Engineering
- No overengineering
- No unnecessary abstractions
- No premature scalability layers
- Keep services small, readable, testable

---

## 1.2 Hard File Size Limit (Python)
- Every Python source file MUST be **< 200 lines**
  - Excluding blank lines + comments
- If logic grows → split into another module immediately

---

## 1.3 Testing is Mandatory
- Every service MUST maintain:
  - **> 80% unit test coverage**
  - `pytest + coverage`
- No feature is complete without tests
- No PR is acceptable without passing test suite

Required test structure:

```
tests/
test_routes.py
test_service.py
test_adapters.py
```


---

## 1.4 Deterministic Outputs (Reproducibility)
Given the same inputs, artifacts MUST be byte-for-byte identical.

Forbidden:
- Random IDs mid-run
- Timestamps generated during pipeline execution
- Floating-point nondeterminism without fixed seed

Allowed:
- Timestamp captured ONCE at session creation and persisted
- Session IDs provided by client

---

## 1.5 Artifact-Driven Execution
Every pipeline step MUST:

1. Write its main artifact to:

```
runtime/sessions/<session_id>/
```

2. Append failures ONLY to:

```
runtime/sessions/<session_id>/errors.log
```


Never fail silently.

---

## 1.6 Communication Model
Services communicate ONLY via:

- HTTP APIs (Flask)
- OpenAPI contracts (`openapi.yaml`)
- Shared disk artifacts

Explicitly forbidden:
- Direct Python imports across services
- Message queues (Kafka/Rabbit)
- Databases (Postgres/MySQL/etc)

---

## 1.7 Runtime Constraints
- Linux-only
- CPU-first
- Docker-first
- Python microservices only

Gunicorn is the production server.

---

# 2. REPOSITORY ARCHITECTURE

## 2.1 Monorepo Layout

```
services/
  transcriber/
  analyzer/
  exporter/

runtime/
  sessions/<session_id>/

docs/
  architecture.md
  context.md
  pipeline-flow.md

.windsurf/rules/
  01-core-rules.md
  02-testing.md
```

---

## 2.2 Standard Service Template

Each service MUST follow:

```
services/<name>/
app.py        # Flask entrypoint (minimal)
routes.py     # HTTP endpoints only (Blueprint)
service.py    # Core business logic / use cases
adapters.py   # External integrations (FS, Whisper, Anki)
openapi.yaml  # Contract-first API definition
tests/        # Unit tests
```


### File Responsibilities

| File         | Allowed Content |
|-------------|----------------|
| app.py       | Flask boot only |
| routes.py    | Request/response mapping only |
| service.py   | Pure business logic |
| adapters.py  | External side effects (fs, AI models, exports) |
| tests/       | Unit coverage for all layers |

---

# 3. SESSION ARTIFACT CONTRACT

Canonical session folder:

```
runtime/sessions/<session_id>/
input.wav
transcript.txt
analysis.json
report.md
anki.apkg
errors.log
```


Rules:
- Artifacts are append-only
- Completed sessions become immutable
- Reprocessing requires a new session ID

---

# 4. WINDSURF RULES ARE PART OF THE CONTRACT

Agents MUST treat all files under:

```
.windsurf/rules/
```


as binding law.

Key enforcement areas:

- Testing discipline
- Git + commit hygiene
- Code quality + linting
- Security + best practices
- PR review simulation
- GitFlow enforcement

Do NOT ignore these rules.

---

# 5. REQUIRED AGENT BEHAVIOR (Codex Operating Mode)

When working in this repo, the agent MUST:

## Step 1 — Read Context First
Always read:

- AGENTS.md (this file)
- docs/architecture.md
- docs/pipeline-flow.md
- .windsurf/rules/*

## Step 2 — Plan Before Writing
Before coding, produce:

- Files to change
- Tests to add
- Expected artifacts

## Step 3 — Generate in Small Commits
Use GitFlow branches:

- feature/<name>
- bugfix/<name>

Conventional commits only:

- feat:
- fix:
- test:
- refactor:
- docs:

## Step 4 — Never Merge Without:
- All tests passing
- Coverage > 80%
- File size compliance (<200 LOC)
- Deterministic artifact guarantee

---

# 6. DEFAULT ERROR HANDLING CONTRACT

On any failure:

- Append a structured line to `errors.log`
- Continue safely if possible
- Never crash without writing the error artifact

Example log line:

```txt
[transcriber] failed: whisper model not available
```
