import pytest
from unittest.mock import Mock, patch
from app.infrastructure.transcriber_factory import TranscriberFactory
from app.infrastructure.whisper_transcriber import WhisperTranscriber
from app.infrastructure.faster_whisper_transcriber import FasterWhisperTranscriber

class TestTranscriberFactoryUpdated:
    
    def test_create_faster_whisper_transcriber(self):
        """Test creating Faster Whisper transcriber."""
        transcriber = TranscriberFactory.create_transcriber("faster-whisper")
        
        assert isinstance(transcriber, FasterWhisperTranscriber)
    
    def test_create_faster_whisper_transcriber_variants(self):
        """Test creating Faster Whisper transcriber with variant names."""
        models = ["faster-whisper", "faster_whisper", "fast-whisper"]
        
        for model in models:
            transcriber = TranscriberFactory.create_transcriber(model)
            assert isinstance(transcriber, FasterWhisperTranscriber)
    
    def test_create_faster_whisper_transcriber_with_custom_path(self):
        """Test creating Faster Whisper transcriber with custom model path."""
        custom_path = "custom-faster-model"
        
        # Test actual creation with custom path
        transcriber = TranscriberFactory.create_transcriber("faster-whisper", model_path=custom_path)
        
        # Verify it's the right type
        assert isinstance(transcriber, FasterWhisperTranscriber)
        # Verify the path was set correctly
        assert transcriber.model_path == custom_path
    
    def test_create_all_transcriber_types(self):
        """Test creating all available transcriber types."""
        expected_types = {
            "whisper": WhisperTranscriber,
            "base": WhisperTranscriber,
            "tiny": WhisperTranscriber,
            "faster-whisper": FasterWhisperTranscriber,
            "fast-whisper": FasterWhisperTranscriber
        }
        
        for model, expected_type in expected_types.items():
            transcriber = TranscriberFactory.create_transcriber(model)
            assert isinstance(transcriber, expected_type)
    
    def test_get_updated_available_models(self):
        """Test getting list of available models includes faster-whisper."""
        models = TranscriberFactory.get_available_models()
        
        expected_models = [
            "whisper", "base", "small", "medium", "large-v3", "tiny",
            "faster-whisper", "fast-whisper"
        ]
        
        assert models == expected_models
        assert len(models) == 8
    
    def test_case_insensitive_faster_whisper_selection(self):
        """Test that faster-whisper selection is case insensitive."""
        models = ["FASTER-WHISPER", "Fast-Whisper", "faster_whisper"]
        
        for model in models:
            transcriber = TranscriberFactory.create_transcriber(model)
            assert isinstance(transcriber, FasterWhisperTranscriber)
    
    def test_priority_order_whisper_over_faster_whisper(self):
        """Test that whisper is selected over faster-whisper when appropriate."""
        whisper_transcriber = TranscriberFactory.create_transcriber("whisper")
        faster_transcriber = TranscriberFactory.create_transcriber("faster-whisper")
        
        assert isinstance(whisper_transcriber, WhisperTranscriber)
        assert isinstance(faster_transcriber, FasterWhisperTranscriber)
        assert whisper_transcriber is not faster_transcriber
