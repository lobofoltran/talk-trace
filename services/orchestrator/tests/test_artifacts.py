from pathlib import Path

from app.infrastructure.artifact_store_fs import ArtifactStore


def test_create_session_creates_errors_log():
    store = ArtifactStore()

    session_dir = store.create_session("session-123")

    assert session_dir.exists()
    assert (session_dir / "errors.log").exists()
