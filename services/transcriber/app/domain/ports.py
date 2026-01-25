from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

class TranscriberPort(ABC):
    @abstractmethod
    def transcribe(self, audio_file: Path, model: str = "base", language: Optional[str] = None) -> str:
        """Transcribe audio file to text."""
        ...

class AudioStorePort(ABC):
    @abstractmethod
    def get_audio_file(self, session_id: str) -> Path:
        """Get audio file path for session."""
        ...
    
    @abstractmethod
    def save_transcript(self, session_id: str, transcript: str) -> None:
        """Save transcript to session artifacts."""
        ...
