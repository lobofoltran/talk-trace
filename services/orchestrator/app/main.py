from fastapi import FastAPI

from app.api.routes.sessions import router as sessions_router
from app.api.routes.health import router as health_router

app = FastAPI(
    title="TalkTrace Orchestrator",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(sessions_router)
