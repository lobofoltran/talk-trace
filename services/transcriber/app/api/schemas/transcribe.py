from pydantic import BaseModel, Field
from typing import Optional

class TranscribeRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    model: str = Field(default="whisper", description="Transcription model (whisper, faster-whisper, base, small, medium, large-v3, tiny)")
    language: Optional[str] = Field(default="auto", description="Language code")

class TranscribeResponse(BaseModel):
    success: bool
    session_id: str
    transcript: Optional[str] = None
    duration: Optional[float] = None
    processing_time: Optional[float] = Field(default=None, description="Time taken for transcription in seconds")
    error: Optional[str] = None
