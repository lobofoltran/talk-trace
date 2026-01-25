import whisper
import librosa
from pathlib import Path
from typing import Optional
from app.domain.ports import TranscriberPort

class WhisperTranscriber(TranscriberPort):
    def __init__(self):
        self._models = {}
    
    def _load_model(self, model_name: str):
        """Load Whisper model if not already loaded."""
        if model_name not in self._models:
            try:
                self._models[model_name] = whisper.load_model(model_name)
            except Exception as e:
                available_models = list(whisper.available_models()) if hasattr(whisper, 'available_models') else []
                raise RuntimeError(f"Whisper model '{model_name}' not found; available models = {available_models}")
        return self._models[model_name]
    
    def transcribe(self, audio_file: Path, model: str = "base", language: Optional[str] = None) -> str:
        """Transcribe audio file using Whisper."""
        try:
            model_instance = self._load_model(model)
            
            # Prepare transcription options
            options = {
                "fp16": False,  # CPU compatibility
                "verbose": False
            }
            
            if language and language != "auto":
                options["language"] = language
            
            result = model_instance.transcribe(str(audio_file), **options)
            return result["text"].strip()
            
        except Exception as e:
            raise RuntimeError(f"Whisper transcription failed: {str(e)}")
    
    def get_audio_duration(self, audio_file: Path) -> float:
        """Get audio duration in seconds using librosa."""
        try:
            duration = librosa.get_duration(path=str(audio_file))
            return round(duration, 2)
        except Exception as e:
            raise RuntimeError(f"Failed to get audio duration: {str(e)}")
