# TalkTrace

**Local-first, artifact-driven speech learning pipeline**

Record → Transcribe → Analyze → Report → Export → Review

## Overview

TalkTrace is a reproducible speech learning system that processes audio recordings through a deterministic pipeline:

1. **Record** audio input
2. **Transcribe** using Whisper models
3. **Analyze** grammar and vocabulary
4. **Report** learning insights
5. **Export** Anki flashcards
6. **Review** in Anki

## Architecture

- **Microservices**: Orchestrator, Transcriber, Analyzer, Exporter
- **Communication**: HTTP APIs + shared disk artifacts
- **Deterministic**: Same inputs → same outputs (byte-for-byte)
- **Local-first**: No external dependencies, runs offline
- **Test-driven**: >80% coverage required

## Session Artifacts

Each session generates immutable artifacts:

```
runtime/sessions/<session_id>/
├── input.wav          # Original audio
├── transcript.txt     # Whisper transcription
├── analysis.json      # Grammar/vocabulary analysis
├── report.md          # Learning report
├── anki.apkg          # Anki flashcard deck
└── errors.log         # Error log (append-only)
```

## Services

### Orchestrator (Port 8000)
- Session management
- Audio recording
- Pipeline coordination

### Transcriber (Port 8001)
- Whisper speech-to-text
- Multiple model sizes
- Language detection

### Analyzer (Port 8002)
- Grammar analysis
- Vocabulary extraction
- Learning insights

### Exporter (Port 8003)
- Anki deck generation
- Flashcard formatting
- Export packaging

## Development

### Code Quality
- Files < 200 lines
- Functions < 30 lines
- Type hints required
- Black + Ruff formatting

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Specific service
pytest services/orchestrator/tests/
```

### Git Workflow
- `main` - production
- `develop` - integration
- `feature/*` - new features
- Conventional commits required