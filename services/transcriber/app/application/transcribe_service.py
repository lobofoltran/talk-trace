from pathlib import Path
from typing import Optional
import time
from app.domain.ports import TranscriberPort, AudioStorePort

class SessionNotFoundError(Exception):
    """Raised when session audio file is not found."""
    pass

class TranscribeService:
    def __init__(
        self,
        transcriber: TranscriberPort,
        audio_store: AudioStorePort
    ):
        self.transcriber = transcriber
        self.audio_store = audio_store
    
    def transcribe_session(
        self, 
        session_id: str, 
        model: str = "base", 
        language: Optional[str] = None
    ) -> dict:
        """Transcribe audio for given session."""
        start_time = time.time()
        
        try:
            # Get audio file
            audio_file = self.audio_store.get_audio_file(session_id)
            
            # Transcribe with timing
            if hasattr(self.transcriber, 'transcribe_with_timing'):
                result = self.transcriber.transcribe_with_timing(audio_file, model, language)
                transcript = result.get("transcript")
                processing_time = result.get("processing_time")
                duration = result.get("duration")
            else:
                transcript = self.transcriber.transcribe(audio_file, model, language)
                processing_time = time.time() - start_time
                duration = None
                if hasattr(self.transcriber, 'get_audio_duration'):
                    try:
                        duration = self.transcriber.get_audio_duration(audio_file)
                    except Exception:
                        pass  # Duration is optional
            
            # Save transcript
            self.audio_store.save_transcript(session_id, transcript)
            
            total_time = time.time() - start_time
            
            return {
                "success": True,
                "session_id": session_id,
                "transcript": transcript,
                "duration": duration,
                "processing_time": round(processing_time, 3),
                "error": None
            }
            
        except FileNotFoundError as e:
            return {
                "success": False,
                "session_id": session_id,
                "transcript": None,
                "duration": None,
                "processing_time": round(time.time() - start_time, 3),
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "session_id": session_id,
                "transcript": None,
                "duration": None,
                "processing_time": round(time.time() - start_time, 3),
                "error": str(e)
            }
