import uuid
from typing import Callable

from app.infrastructure.artifact_store_fs import ArtifactStore
from app.domain.ports import RecorderPort

class SessionService:
    def __init__(
        self,
        store: ArtifactStore | None = None,
        recorder_factory: Callable = None,
    ):
        self.store = store or ArtifactStore()
        self.recorders: dict[str, RecorderPort] = {}
        self.recorder_factory = recorder_factory

    def start_session(self) -> str:
        session_id = str(uuid.uuid4())
        session_dir = self.store.create_session(session_id)
        recorder = self.recorder_factory(session_dir / "input.wav")
        recorder.start()
        self.recorders[session_id] = recorder

        return session_id

    def finish_session(self, session_id: str):
        recorder = self.recorders.get(session_id)
        
        if not recorder:
            raise RuntimeError("Session not active")

        recorder.stop()
        del self.recorders[session_id]
