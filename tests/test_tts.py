import pytest
from fastapi.testclient import TestClient
import os
import tempfile

from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/tts/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_voices():
    response = client.get("/api/tts/voices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Check if we have at least one engine with voices
    engines_with_voices = [e for e in response.json() if len(e["voices"]) > 0]
    assert len(engines_with_voices) > 0

def test_text_to_speech_gtts():
    # Using a temp dir to avoid file conflicts
    with tempfile.TemporaryDirectory() as temp_dir:
        # Temporarily override the audio directory
        os.environ["TTS_OUTPUT_DIR"] = temp_dir
        
        request_data = {
            "text": "This is a test message for the TTS API.",
            "engine": "gtts",
            "language": "en",
            "speed": 1.0
        }
        
        response = client.post("/api/tts", json=request_data)
        
        # Clean up env var
        os.environ.pop("TTS_OUTPUT_DIR", None)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["audio_url"].startswith("/static/audio/")
        assert data["text_preview"] == request_data["text"]
        assert isinstance(data["processing_time"], float)