# app/main.py
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from .tts_engine import TTSEngine

app = FastAPI(title="Text-to-Speech API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create TTS engine instances
gtts_engine = TTSEngine(engine_type="gtts")
pyttsx3_engine = TTSEngine(engine_type="pyttsx3")

class TTSRequest(BaseModel):
    text: str
    engine: str = "gtts"  # "gtts" or "pyttsx3"
    language: str = "en"
    voice: Optional[str] = None
    speed: float = 1.0

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech and return URL to the audio file"""
    try:
        if request.engine == "gtts":
            filename = gtts_engine.generate_speech(
                request.text, 
                lang=request.language,
                speed=request.speed
            )
        else:
            filename = pyttsx3_engine.generate_speech(
                request.text,
                voice=request.voice,
                speed=request.speed
            )
        
        audio_url = f"/static/audio/{filename}"
        return {"status": "success", "audio_url": audio_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@app.get("/voices")
async def get_voices():
    """Get available voices (for pyttsx3)"""
    try:
        # Initialize pyttsx3 and get voices
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        voice_list = [
            {"id": voice.id, "name": voice.name, "languages": voice.languages}
            for voice in voices
        ]
        
        return {"voices": voice_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voices: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Text-to-Speech API"}