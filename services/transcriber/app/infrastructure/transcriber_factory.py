from pathlib import Path
from typing import Optional
from app.domain.ports import TranscriberPort
from app.infrastructure.whisper_transcriber import WhisperTranscriber
from app.infrastructure.faster_whisper_transcriber import FasterWhisperTranscriber

class TranscriberFactory:
    """Factory for creating transcriber instances based on model type."""
    
    @staticmethod
    def create_transcriber(model: str = "whisper", **kwargs) -> TranscriberPort:
        """
        Create transcriber instance based on model type.
        
        Args:
            model: Model type ("whisper", "faster-whisper", or specific model names)
            **kwargs: Additional parameters for transcriber initialization
            
        Returns:
            TranscriberPort instance
        """
        model_lower = model.lower()
        
        if model_lower in ["faster-whisper", "faster_whisper", "fast-whisper"]:
            return FasterWhisperTranscriber(
                model_path=kwargs.get("model_path", "tiny")
            )
        elif model_lower in ["whisper", "base", "small", "medium", "large-v3", "tiny"]:
            return WhisperTranscriber()
        else:
            # Default to Whisper for unknown models
            return WhisperTranscriber()
    
    @staticmethod
    def get_available_models() -> list[str]:
        """Get list of available model types."""
        return [
            "whisper", "base", "small", "medium", "large-v3", "tiny",
            "faster-whisper", "fast-whisper"
        ]
