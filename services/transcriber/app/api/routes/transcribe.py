from fastapi import APIRouter, HTTPException
from app.api.schemas.transcribe import TranscribeRequest, TranscribeResponse
from app.application.transcribe_service import TranscribeService, SessionNotFoundError
from app.infrastructure.transcriber_factory import TranscriberFactory
from app.infrastructure.audio_store_fs import AudioStore

router = APIRouter(prefix="/transcribe", tags=["transcribe"])

# Strategy pattern - select transcriber based on request
def get_transcriber(model: str):
    """Strategy selector for transcriber based on model type."""
    return TranscriberFactory.create_transcriber(model)

audio_store = AudioStore()

@router.post("", response_model=TranscribeResponse)
def transcribe(request: TranscribeRequest) -> TranscribeResponse:
    """Transcribe audio file for session."""
    try:
        # Strategy pattern: select transcriber based on model
        transcriber = get_transcriber(request.model)
        service = TranscribeService(transcriber, audio_store)
        
        result = service.transcribe_session(
            session_id=request.session_id,
            model=request.model,
            language=request.language
        )
        
        return TranscribeResponse(**result)
        
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
