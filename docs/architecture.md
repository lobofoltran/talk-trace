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

TalkTrace is intentionally **not** a SaaS platform.
It is a reproducible CLI + microservice pipeline.

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

The system is split into small Python services:

* orchestrator (recording + session control)
* transcriber
* analyzer
* exporter

Each service is:

* isolated
* HTTP-only
* contract-first via OpenAPI
* independently testable

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

No feature is complete without tests.

---

# System Architecture

## High-Level Flow

```
┌──────────────┐
│ Orchestrator │  (entrypoint)
│ Recorder     │
└────┬─────────┘
     │ creates session + input.wav
     ▼
┌──────────────┐
│ Transcriber  │  → transcript.txt
└────┬─────────┘
     ▼
┌──────────────┐
│ Analyzer     │  → analysis.json + report.md
└────┬─────────┘
     ▼
┌──────────────┐
│ Exporter     │  → anki.apkg
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

## 1. Orchestrator (Recorder + Session Finalizer)

**Purpose:** Entry-point service that manages the full session lifecycle.

### Responsibilities

* Create session directory
* Capture audio via ffmpeg
* Write `input.wav`
* Call pipeline services in order:

  1. transcriber
  2. analyzer
  3. exporter
* Finalize session by writing `completed.json`
* Append errors to `errors.log`

### Boundary

* Does NOT transcribe
* Does NOT analyze
* Does NOT export flashcards
* Only coordinates

---

## 2. Transcriber Service

**Purpose:** Convert raw audio into text.

### Input Artifact

* `input.wav`

### Output Artifact

* `transcript.txt`

### Responsibilities

* Run speech-to-text transcription (Whisper adapter)
* Write deterministic transcript output
* Append failures to `errors.log`

### Boundary

* No grammar analysis
* Only transcription

---

## 3. Analyzer Service

**Purpose:** Analyze transcript and generate learning feedback.

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

Any deviation from determinism, testing discipline, or contract-first design is considered a contract violation.
