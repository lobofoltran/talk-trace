from fastapi import APIRouter
from app.api.schemas.sessions import StartSessionResponse
from app.application.session_service import SessionService
from app.infrastructure.artifact_store_fs import ArtifactStore
from app.infrastructure.recorder_ffmpeg import FFmpegRecorder

router = APIRouter(prefix="/session")

def recorder_factory(output_path):
    return FFmpegRecorder(output_path)

service = SessionService(
    store=ArtifactStore(),
    recorder_factory=recorder_factory
)

@router.post("", response_model=StartSessionResponse)
def start():
    session_id = service.start_session()
    return {"session_id": session_id}


@router.post("/{session_id}/finish")
def finish(session_id: str):
    service.finish_session(session_id)
    return {"status": "finished"}
