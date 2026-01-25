# TalkTrace Transcriber

FastAPI service for speech-to-text transcription using OpenAI Whisper models.

## Overview

The Transcriber service converts audio recordings to text using state-of-the-art Whisper models. It follows Clean Architecture principles with dependency injection and comprehensive testing.

## Features

- **Multiple Whisper Models**: tiny, base, small, medium, large-v3
- **Language Support**: Auto-detection or specific language codes
- **Clean Architecture**: Ports & Adapters pattern
- **Type Safety**: Full Pydantic validation
- **Error Handling**: Proper HTTP status codes
- **Comprehensive Testing**: 10/10 tests passing

## Architecture

```
app/
├── api/                    # FastAPI layer
│   ├── routes/            # HTTP endpoints
│   └── schemas/           # Pydantic models
├── application/           # Use cases
├── domain/               # Business logic & ports
├── infrastructure/       # External integrations
└── config/               # Settings
```

## Quick Start

### Installation

```bash
cd services/transcriber
pip install -r requirements.txt
```

### Run Development Server

```bash
uvicorn app.main:app --port 8001 --reload
```

### Run Tests

```bash
pytest tests/ -v
```

## API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

### Endpoints

#### POST /transcribe
Transcribe audio file for a session.

**Request:**
```json
{
  "session_id": "uuid-string",
  "model": "base",
  "language": "auto"
}
```

**Response (Success):**
```json
{
  "success": true,
  "session_id": "uuid-string",
  "transcript": "Transcribed text here...",
  "duration": 15.5,
  "error": null
}
```

**Response (Session Not Found):**
```json
{
  "detail": "Audio file not found"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "talktrace-transcriber"
}
```

## Session Artifacts

The service expects audio files in the standard TalkTrace session structure:

```
runtime/sessions/<session_id>/
├── input.wav          # Audio file to transcribe
├── transcript.txt    # Generated transcript
└── errors.log         # Error log
```

## Configuration

### Environment Variables

- `SESSIONS_DIR`: Path to sessions directory (default: `../../runtime/sessions`)

### Whisper Models

Available models (ordered by size/accuracy):
- `tiny`: Fastest, lowest accuracy
- `base`: Good balance
- `small`: Better accuracy
- `medium`: High accuracy
- `large-v3`: Best accuracy

### Language Codes

Common language codes:
- `en`: English
- `pt`: Portuguese  
- `es`: Spanish
- `fr`: French
- `de`: German
- `auto`: Auto-detect (default)

## Development

### Code Quality

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# Type checking
mypy app/
```

### Project Structure

The service follows Clean Architecture with:

- **Ports**: Abstract interfaces (`TranscriberPort`, `AudioStorePort`)
- **Adapters**: Concrete implementations (`WhisperTranscriber`, `AudioStore`)
- **Use Cases**: Business logic (`TranscribeService`)
- **Controllers**: HTTP layer (`routes/`)

## Error Handling

- **404**: Session/audio file not found
- **422**: Request validation error
- **500**: Internal server error

All errors follow FastAPI's standard error response format.

## Dependencies

- **FastAPI**: Web framework
- **OpenAI Whisper**: Speech-to-text models
- **Librosa**: Audio processing
- **Pydantic**: Data validation
- **Pytest**: Testing framework

## License

MIT License - see project root for details.
