from fastapi import FastAPI

from app.api.routes.transcribe import router as transcribe_router
from app.api.routes.health import router as health_router

app = FastAPI(
    title="TalkTrace Transcriber",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(transcribe_router)
