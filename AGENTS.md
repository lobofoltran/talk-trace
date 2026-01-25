# AGENTS.md — TalkTrace Agent Contract (Codex-First)

**Local-first, artifact-driven speech learning pipeline using Clean Architecture**

Record → Transcribe → Analyze → Report → Export → Review

This repository is designed to be operated by AI agents (Codex, GPT, Claude) with strict architectural discipline.

---

# 1. NON-NEGOTIABLE RULES (MUST)

## 1.1 Clean Architecture is MANDATORY
- **All services MUST follow Clean Architecture**
- **Dependency Direction**: Inward only (Domain ← Application ← Infrastructure ← API)
- **No circular dependencies** between layers
- **Interface segregation** in domain layer
- **Never import from outer layers** (e.g., API cannot import from Infrastructure)

---

## 1.2 Minimal + Pragmatic Engineering
- No overengineering
- No unnecessary abstractions
- No premature scalability layers
- Keep services small, readable, testable

---

## 1.3 Hard File Size Limit (Python)
- Every Python source file MUST be **< 200 lines**
  - Excluding blank lines + comments
- If logic grows → split into another module immediately

---

## 1.4 Testing is Mandatory
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

## 1.5 Deterministic Outputs (Reproducibility)
Given the same inputs, artifacts MUST be byte-for-byte identical.

Forbidden:
- Random IDs mid-run
- Timestamps generated during pipeline execution
- Floating-point nondeterminism without fixed seed

Allowed:
- Timestamp captured ONCE at session creation and persisted
- Session IDs provided by client

---

## 1.6 Artifact-Driven Execution
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

## 1.7 Communication Model
Services communicate ONLY via:

- HTTP APIs (FastAPI)
- OpenAPI contracts (`openapi.yaml`)
- Shared disk artifacts

Explicitly forbidden:
- Direct Python imports across services
- Message queues (Kafka/Rabbit)
- Databases (Postgres/MySQL/etc)

---

## 1.8 Runtime Constraints
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

## 2.2 Standard Service Template (Clean Architecture)

Each service MUST follow:

```
services/<name>/
├── app/
│   ├── api/
│   │   └── routes/            # HTTP endpoints, request/response mapping
│   ├── application/           # Use cases, orchestrators, business rules
│   ├── domain/                # Business logic, entities, ports (interfaces)
│   └── infrastructure/        # External integrations, adapters, implementations
├── app.py                     # FastAPI entrypoint (minimal)
├── openapi.yaml              # Contract-first API definition
└── tests/                    # Unit tests
```

### Clean Architecture Layer Responsibilities

| Layer | Responsibilities | Forbidden |
|-------|------------------|------------|
| **API** | HTTP endpoints, request/response mapping | Business logic, external dependencies |
| **Application** | Use cases, orchestrators, business rules | Direct external calls, HTTP frameworks |
| **Domain** | Business logic, entities, ports (interfaces) | External dependencies, frameworks |
| **Infrastructure** | External integrations, adapters, implementations | Business logic |

### File Responsibilities

| File | Allowed Content |
|------|----------------|
| app.py | FastAPI boot only |
| app/api/routes/ | Request/response mapping only |
| app/application/ | Use cases, business rules |
| app/domain/ | Business logic, entities, ports |
| app/infrastructure/ | External side effects (fs, AI models, exports) |
| tests/ | Unit coverage for all layers |

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
- **Clean Architecture compliance**

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
- **Clean Architecture layer placement**

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
- **Clean Architecture compliance**

---

# 6. CLEAN ARCHITECTURE CHECKLIST

Before completing any task, verify:

## 6.1 Layer Separation
- [ ] API layer only handles HTTP concerns
- [ ] Application layer contains use cases
- [ ] Domain layer has pure business logic
- [ ] Infrastructure layer handles external integrations

## 6.2 Dependency Rules
- [ ] Dependencies flow inward only
- [ ] No circular dependencies
- [ ] Domain layer has no external dependencies
- [ ] API layer doesn't import from Infrastructure

## 6.3 Interface Design
- [ ] Interfaces defined in domain layer
- [ ] Implementations in infrastructure layer
- [ ] Dependency injection used throughout
- [ ] Interface segregation followed

---

# 7. DEFAULT ERROR HANDLING CONTRACT

On any failure:

- Append a structured line to `errors.log`
- Continue safely if possible
- Never crash without writing the error artifact

Example log line:

```txt
[transcriber] failed: whisper model not available
```

---

# 8. CLEAN ARCHITECTURE BENEFITS

## 8.1 Testability
- Each layer can be tested independently
- External dependencies are easily mocked
- Business logic is isolated from infrastructure

## 8.2 Maintainability
- Clear separation of concerns
- Dependencies flow inward
- Easy to understand and modify

## 8.3 Flexibility
- Easy to swap implementations (e.g., different transcribers)
- Business logic doesn't depend on external systems
- Interface-based design allows multiple implementations

---

**Remember: Clean Architecture is not optional - it's mandatory for all services in TalkTrace!**
