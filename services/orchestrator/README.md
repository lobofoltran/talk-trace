# TalkTrace Orchestrator

FastAPI service responsible for:

- Session creation
- Audio recording via ffmpeg
- Artifact-driven pipeline coordination

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```

## Docs

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## API

### Start session

```http
curl -X POST http://localhost:8000/session
```

### Finish session

```http
curl -X POST http://localhost:8000/session/<uuid>/finish
```

Artifacts stored in:

```
runtime/sessions/<uuid>/
```