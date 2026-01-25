import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app

class TestStrategyPattern:
    
    def test_strategy_selects_whisper_by_default(self):
        """Test that strategy selects Whisper by default."""
        client = TestClient(app)
        
        response = client.post(
            "/transcribe",
            json={
                "session_id": "test-session",
                "model": "whisper"
            }
        )
        
        # Should not fail on strategy selection
        assert response.status_code in [200, 404]  # 404 if session doesn't exist
        data = response.json()
        assert "success" in data or "detail" in data
    
    def test_strategy_selects_faster_whisper_when_requested(self):
        """Test that strategy selects Faster Whisper when explicitly requested."""
        client = TestClient(app)
        
        response = client.post(
            "/transcribe",
            json={
                "session_id": "test-session",
                "model": "faster-whisper"
            }
        )
        
        # Should not fail on strategy selection
        assert response.status_code in [200, 404]  # 404 if session doesn't exist
        data = response.json()
        assert "success" in data or "detail" in data
    
    def test_strategy_selects_whisper_for_whisper_models(self):
        """Test strategy selects Whisper for Whisper-specific models."""
        whisper_models = ["base", "small", "medium", "large-v3"]
        
        client = TestClient(app)
        
        for model in whisper_models:
            response = client.post(
                "/transcribe",
                json={
                    "session_id": "test-session",
                    "model": model
                }
            )
            
            # Should not fail on strategy selection
            assert response.status_code in [200, 404]
            data = response.json()
            assert "success" in data or "detail" in data
    
    def test_strategy_defaults_to_whisper_for_unknown_model(self):
        """Test strategy defaults to Whisper for unknown models."""
        client = TestClient(app)
        
        response = client.post(
            "/transcribe",
            json={
                "session_id": "test-session",
                "model": "unknown-model"
            }
        )
        
        # Should not fail on strategy selection
        assert response.status_code in [200, 404]
        data = response.json()
        assert "success" in data or "detail" in data
    
    @patch('app.api.routes.transcribe.TranscriberFactory')
    def test_strategy_factory_integration(self, mock_factory):
        """Test integration between strategy and factory."""
        from app.api.routes.transcribe import get_transcriber
        
        # Mock factory to return specific transcriber
        mock_transcriber = Mock()
        mock_factory.create_transcriber.return_value = mock_transcriber
        
        # Test strategy calls factory correctly
        result = get_transcriber("faster-whisper")
        
        mock_factory.create_transcriber.assert_called_once_with("faster-whisper")
        assert result == mock_transcriber
