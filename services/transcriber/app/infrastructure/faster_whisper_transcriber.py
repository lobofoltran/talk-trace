import time
from pathlib import Path
from typing import Optional
from app.domain.ports import TranscriberPort

class FasterWhisperTranscriber(TranscriberPort):
    def __init__(self, model_path: str = None):
        """
        Initialize Faster Whisper transcriber.
        
        Args:
            model_path: Path to Faster Whisper model. If None, will use default.
        """
        self.model_path = model_path or "tiny"
        self._model = None
    
    def _load_model(self):
        """Load Faster Whisper model if not already loaded."""
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
                self._model = WhisperModel(self.model_path, compute_type="float32")
            except ImportError:
                raise RuntimeError(
                    "faster-whisper not installed. Install with: "
                    "pip install faster-whisper"
                )
            except Exception as e:
                raise RuntimeError(f"Failed to create Faster Whisper model: {str(e)}")
        return self._model
    
    def transcribe(self, audio_file: Path, model: str = "tiny", language: Optional[str] = None) -> str:
        """Transcribe audio file using Faster Whisper."""
        start_time = time.time()
        
        try:
            model_instance = self._load_model()
            
            # Transcribe with faster-whisper
            segments, info = model_instance.transcribe(
                str(audio_file),
                language=language if language and language != "auto" else None,
                beam_size=5,
                best_of=5,
                temperature=0.0,
                word_timestamps=False
            )
            
            # Combine all segments
            transcript = " ".join(segment.text for segment in segments).strip()
            
            return transcript
            
        except Exception as e:
            raise RuntimeError(f"Faster Whisper transcription failed: {str(e)}")
    
    def transcribe_with_timing(self, audio_file: Path, model: str = "tiny", language: Optional[str] = None) -> dict:
        """Transcribe audio file and return result with timing information."""
        start_time = time.time()
        
        try:
            transcript = self.transcribe(audio_file, model, language)
            processing_time = time.time() - start_time
            
            return {
                "transcript": transcript,
                "processing_time": round(processing_time, 3)
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "transcript": None,
                "processing_time": round(processing_time, 3),
                "error": str(e)
            }
    
    def get_audio_duration(self, audio_file: Path) -> float:
        """Get audio duration in seconds."""
        try:
            model_instance = self._load_model()
            
            # Get duration using faster-whisper
            _, info = model_instance.transcribe(str(audio_file), language=None)
            duration = info.duration
            
            return round(duration, 2)
        except Exception as e:
            raise RuntimeError(f"Failed to get audio duration: {str(e)}")
