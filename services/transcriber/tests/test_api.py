from fastapi import HTTPException
from fastapi.testclient import TestClient

def test_transcribe_endpoint_success(client):
    response = client.post(
        "/transcribe",
        json={
            "session_id": "test-session",
            "model": "base",
            "language": "en"
        }
    )
    
    # Should return 200 with success: false since no audio file exists
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Audio file not found" in data["error"]
    assert "processing_time" in data

def test_transcribe_endpoint_missing_session_id(client):
    response = client.post(
        "/transcribe",
        json={
            "model": "base"
        }
    )
    
    assert response.status_code == 422  # Validation error

def test_transcribe_endpoint_default_values(client):
    response = client.post(
        "/transcribe",
        json={
            "session_id": "test-session"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["session_id"] == "test-session"
    assert "processing_time" in data
