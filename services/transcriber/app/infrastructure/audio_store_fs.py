from pathlib import Path
from app.config.settings import SESSIONS_DIR
from app.domain.ports import AudioStorePort

class AudioStore(AudioStorePort):
    def __init__(self, base_dir: Path = SESSIONS_DIR):
        self.base_dir = base_dir

    def get_audio_file(self, session_id: str) -> Path:
        audio_file = self.base_dir / session_id / "input.wav"
        
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found")
        
        return audio_file

    def save_transcript(self, session_id: str, transcript: str) -> None:
        transcript_file = self.base_dir / session_id / "transcript.txt"
        
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)
