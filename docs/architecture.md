# TalkTrace Architecture

## Overview

TalkTrace is a **local-first, artifact-driven speech learning pipeline**:

Record → Transcribe → Analyze → Report → Export → Review

The system is designed for:

* deterministic execution
* minimal infrastructure
* strict testability
* AI-agent operability (Codex/GPT)
* Linux + CPU-first runtime
* Clean Architecture principles

TalkTrace is intentionally **not** a SaaS platform.
It is a reproducible CLI + microservice pipeline.

---

# Clean Architecture Implementation

## Architecture Layers

All services follow Clean Architecture with strict dependency rules:

```
services/<service>/
├── app/
│   ├── api/                    # Outermost layer
│   │   └── routes/            # HTTP endpoints, request/response mapping
│   ├── application/           # Use cases, orchestrators, business rules
│   ├── domain/                # Innermost layer - business logic, entities, ports
│   └── infrastructure/        # External integrations, adapters, implementations
└── tests/
```

## Dependency Direction

**Inward only**: Domain ← Application ← Infrastructure ← API

* **Domain**: Pure business logic, entities, ports (interfaces)
* **Application**: Use cases, orchestrators, business rules
* **Infrastructure**: External integrations, adapters, implementations
* **API**: HTTP endpoints, request/response mapping

### Key Rules

* **No circular dependencies** between layers
* **Interface segregation** in domain layer
* **Dependency injection** for all external dependencies
* **Never import from outer layers** (e.g., API cannot import from Infrastructure)

---

# Core Principles

## 1. Artifact-Driven, Not Database-Driven

TalkTrace does not use a database.

Instead, the system is built around immutable session artifacts:

```
runtime/sessions/<session_id>/
  input.wav
  transcript.txt
  analysis.json
  report.md
  anki.apkg
  errors.log
```

Artifacts are:

* append-only
* deterministic
* replayable
* easy to debug

---

## 2. Determinism as a Hard Requirement

Given the same inputs, outputs must be byte-for-byte identical.

Forbidden:

* timestamps generated mid-run
* random IDs
* nondeterministic ordering

Allowed:

* timestamp captured once at session creation
* client-provided session IDs

---

## 3. Minimal Microservices, Clear Boundaries

The system is split into small Python services using Clean Architecture:

* recorder (recording + session control)
* transcriber
* analyzer
* exporter

Each service is:

* isolated
* HTTP-only
* contract-first via OpenAPI
* independently testable
* **Clean Architecture compliant**

No cross-importing between services is allowed.

---

## 4. Contract-First APIs

Every service defines its API in:

```
services/<service>/openapi.yaml
```

OpenAPI is the source of truth.

No undocumented endpoints may exist.

---

## 5. Strict Testing Discipline

Every service must maintain:

* pytest unit tests
* > 80% coverage
* full route + schema coverage
* Clean Architecture testing (mock external dependencies)

No feature is complete without tests.

---

# System Architecture

## High-Level Flow

```
┌──────────────┐
│ Recorder     │  (entrypoint)
│ (Clean Arch) │
└────┬─────────┘
     │ creates session + input.wav
     ▼
┌──────────────┐
│ Transcriber  │  → transcript.txt
│ (Clean Arch) │
└────┬─────────┘
     ▼
┌──────────────┐
│ Analyzer     │  → analysis.json + report.md
│ (Clean Arch) │
└────┬─────────┘
     ▼
┌──────────────┐
│ Exporter     │  → anki.apkg
│ (Clean Arch) │
└────┬─────────┘
     ▼
┌──────────┐
│ Review   │ (Anki / Markdown)
└──────────┘
```

All steps communicate only via:

* HTTP calls
* shared artifacts on disk

---

# Service Responsibilities

## 1. Recorder Service

**Purpose:** Entry-point service that manages audio recording and session creation.

### Clean Architecture Structure

```
services/recorder/
├── app/
│   ├── api/routes/
│   │   └── sessions.py      # HTTP endpoints for session management
│   ├── application/
│   │   └── session_service.py  # Use cases for session lifecycle
│   ├── domain/
│   │   ├── entities.py     # Session entity
│   │   └── ports.py         # Interfaces for recording, storage
│   └── infrastructure/
│       ├── adapters.py     # FFmpeg recording implementation
│       └── storage.py       # File system storage implementation
```

### Responsibilities

* Create session directory
* Capture audio via ffmpeg
* Write `input.wav`
* Manage session lifecycle

### Boundary

* Does NOT transcribe
* Does NOT analyze
* Does NOT export flashcards
* Only coordinates recording

---

## 2. Transcriber Service

**Purpose:** Convert raw audio into text.

### Clean Architecture Structure

```
services/transcriber/
├── app/
│   ├── api/routes/
│   │   └── transcribe.py    # HTTP endpoints for transcription
│   ├── application/
│   │   └── transcribe_service.py  # Use cases for transcription
│   ├── domain/
│   │   ├── entities.py     # Transcription entity
│   │   └── ports.py         # Transcriber interface
│   └── infrastructure/
│       ├── adapters.py     # Whisper, Faster-Whisper implementations
│       └── factory.py      # Transcriber factory pattern
```

### Input Artifact

* `input.wav`

### Output Artifact

* `transcript.txt`

### Responsibilities

* Run speech-to-text transcription (Whisper + Faster-Whisper adapters)
* Factory pattern for transcriber selection
* Strategy pattern for runtime selection
* Write deterministic transcript output
* Append failures to `errors.log`

### Boundary

* No grammar analysis
* Only transcription

---

## 3. Analyzer Service

**Purpose:** Analyze transcript and generate learning feedback.

### Clean Architecture Structure

```
services/analyzer/
├── app/
│   ├── api/routes/
│   │   └── analyze.py       # HTTP endpoints for analysis
│   ├── application/
│   │   └── analysis_service.py  # Use cases for analysis
│   ├── domain/
│   │   ├── entities.py     # Analysis entity, patterns
│   │   └── ports.py         # Analyzer interface
│   └── infrastructure/
│       ├── adapters.py     # Grammar analysis implementation
│       └── generators.py   # Report generation
```

### Input Artifact

* `transcript.txt`

### Output Artifacts

* `analysis.json`
* `report.md`

### Responsibilities

* Detect grammar mistakes
* Extract vocabulary + corrections
* Produce structured JSON analysis
* Generate Markdown report
* Append failures to `errors.log`

### Boundary

* Does not export Anki decks
* Pure analysis only

---

## 4. Exporter Service

**Purpose:** Convert analysis into Anki study material.

### Clean Architecture Structure

```
services/exporter/
├── app/
│   ├── api/routes/
│   │   └── export.py        # HTTP endpoints for export
│   ├── application/
│   │   └── export_service.py  # Use cases for export
│   ├── domain/
│   │   ├── entities.py     # Export entity, card structure
│   │   └── ports.py         # Exporter interface
│   └── infrastructure/
│       ├── adapters.py     # Anki deck generation
│       └── formatters.py   # CSV, JSON export implementations
```

### Input Artifacts

* `analysis.json`
* `report.md`

### Output Artifact

* `anki.apkg`

### Responsibilities

* Transform corrections into flashcards
* Package cards into an Anki deck
* Ensure stable ordering + deterministic exports
* Append failures to `errors.log`

### Boundary

* No transcription or analysis
* Export only

---

# Session Model

## Session Lifecycle

Rules:

* session artifacts are immutable once completed
* reruns require new session ID
* all errors go to errors.log

---

# Deployment Architecture

## Docker-First Execution

All services run via Docker Compose.

Constraints:

* Linux-only
* CPU-first
* no GPU-only dependencies

Production server:

* Gunicorn

---

# Clean Architecture Benefits

## 1. Testability
* Each layer can be tested independently
* External dependencies are easily mocked
* Business logic is isolated from infrastructure

## 2. Maintainability
* Clear separation of concerns
* Dependencies flow inward
* Easy to understand and modify

## 3. Flexibility
* Easy to swap implementations (e.g., different transcribers)
* Business logic doesn't depend on external systems
* Interface-based design allows multiple implementations

---

# Key Documents

* `AGENTS.md` — agent contract
* `docs/context.md` — motivation + goals
* `docs/pipeline-flow.md` — execution details
* `.windsurf/rules/*` — enforcement rules

---

## Final Note

TalkTrace is designed as:

* a reproducible learning pipeline
* an AI-agent friendly codebase
* a minimal deterministic system
* a Clean Architecture implementation

Any deviation from determinism, testing discipline, contract-first design, or Clean Architecture principles is considered a contract violation.
