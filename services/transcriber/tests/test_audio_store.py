import pytest
import tempfile
from pathlib import Path
from app.infrastructure.audio_store_fs import AudioStore

def test_get_audio_file_success(tmp_path: Path):
    # Setup
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    session_dir = sessions_dir / "test-session"
    session_dir.mkdir()
    
    audio_file = session_dir / "input.wav"
    audio_file.write_bytes(b"fake audio data")
    
    store = AudioStore(sessions_dir)
    
    # Test
    result = store.get_audio_file("test-session")
    
    assert result == audio_file
    assert result.exists()

def test_get_audio_file_not_found(tmp_path: Path):
    # Setup
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    
    store = AudioStore(sessions_dir)
    
    # Test
    with pytest.raises(FileNotFoundError) as exc_info:
        store.get_audio_file("non-existent")
    
    assert "Audio file not found" in str(exc_info.value)

def test_save_transcript(tmp_path: Path):
    # Setup
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    session_dir = sessions_dir / "test-session"
    session_dir.mkdir()
    
    store = AudioStore(sessions_dir)
    transcript = "Hello world transcript"
    
    # Test
    store.save_transcript("test-session", transcript)
    
    # Verify
    transcript_file = session_dir / "transcript.txt"
    assert transcript_file.exists()
    assert transcript_file.read_text(encoding="utf-8") == transcript
