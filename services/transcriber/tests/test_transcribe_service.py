import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from app.application.transcribe_service import TranscribeService, SessionNotFoundError
from app.domain.ports import TranscriberPort, AudioStorePort

class FakeTranscriber:
    def __init__(self):
        self.transcripts = {
            "base": "Hello world transcript",
            "small": "Small model transcript"
        }
    
    def transcribe(self, audio_file: Path, model: str = "base", language=None) -> str:
        return self.transcripts.get(model, "Default transcript")
    
    def get_audio_duration(self, audio_file: Path) -> float:
        return 15.5

class FakeAudioStore:
    def __init__(self):
        self.transcripts = {}
    
    def get_audio_file(self, session_id: str) -> Path:
        return Path(f"/fake/path/{session_id}/input.wav")
    
    def save_transcript(self, session_id: str, transcript: str) -> None:
        self.transcripts[session_id] = transcript

def test_transcribe_session_success():
    transcriber = FakeTranscriber()
    audio_store = FakeAudioStore()
    service = TranscribeService(transcriber, audio_store)
    
    result = service.transcribe_session("test-session", "base", "en")
    
    assert result["success"] is True
    assert result["session_id"] == "test-session"
    assert result["transcript"] == "Hello world transcript"
    assert result["duration"] == 15.5
    assert audio_store.transcripts["test-session"] == "Hello world transcript"

def test_transcribe_session_audio_not_found():
    transcriber = FakeTranscriber()
    audio_store = FakeAudioStore()
    
    # Mock get_audio_file to raise FileNotFoundError
    audio_store.get_audio_file = Mock(side_effect=FileNotFoundError("Audio not found"))
    
    service = TranscribeService(transcriber, audio_store)
    
    result = service.transcribe_session("non-existent")
    
    assert result["success"] is False
    assert "Audio not found" in result["error"]
    assert result["processing_time"] is not None

def test_transcribe_session_transcriber_error():
    transcriber = FakeTranscriber()
    audio_store = FakeAudioStore()
    
    # Mock transcribe to raise exception
    transcriber.transcribe = Mock(side_effect=RuntimeError("Whisper failed"))
    
    service = TranscribeService(transcriber, audio_store)
    
    result = service.transcribe_session("test-session")
    
    assert result["success"] is False
    assert "Whisper failed" in result["error"]
