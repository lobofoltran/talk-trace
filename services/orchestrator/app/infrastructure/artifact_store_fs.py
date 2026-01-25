from pathlib import Path
import shutil

from app.config.settings import SESSIONS_DIR

class ArtifactStore:
    def __init__(self, base_dir: Path = SESSIONS_DIR):
        self.base_dir = base_dir

    def create_session(self, session_id: str) -> Path:
        session_dir = self.base_dir / session_id

        if session_dir.exists():
            shutil.rmtree(session_dir)

        session_dir.mkdir(parents=True)

        (session_dir / "errors.log").touch()

        return session_dir
