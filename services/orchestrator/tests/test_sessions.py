from pathlib import Path
from app.application.session_service import SessionService
from app.infrastructure.artifact_store_fs import ArtifactStore

class FakeRecorder:
    def __init__(self, output: Path):
        self.output = output
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


def test_start_session_creates_recorder():
    store = ArtifactStore()

    service = SessionService(
        store=store,
        recorder_factory=lambda out: FakeRecorder(out),
    )

    session_id = service.start_session()

    assert session_id in service.recorders
    assert service.recorders[session_id].started is True


def test_finish_session_stops_recorder():
    store = ArtifactStore()

    service = SessionService(
        store=store,
        recorder_factory=lambda out: FakeRecorder(out),
    )

    session_id = service.start_session()

    service.finish_session(session_id)

    assert session_id not in service.recorders
