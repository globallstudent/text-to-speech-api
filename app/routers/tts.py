from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from app.routers.schemas import *

import os
import logging
import time
import asyncio
from datetime import datetime

from app.tts_engine import TTSEngine

router = APIRouter(
    prefix="/api/tts",
    tags=["TTS"],
)

logger = logging.getLogger(__name__)


tts_engine = TTSEngine()


# Global statistics
total_requests = 0
last_request_time = None
start_time = time.time()

def cleanup_old_files(directory="static/audio", max_age_hours=24):
    """Remove audio files older than max_age_hours"""
    try:
        current_time = time.time()
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filename.endswith('.mp3'):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_hours * 3600:
                    os.remove(filepath)
                    logger.info(f"Removed old audio file: {filename}")
    except Exception as e:
        logger.error(f"Error cleaning up old files: {e}")

@router.post("", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    """Convert text to speech and return URL to the audio file"""
    global total_requests, last_request_time
    start_time = time.time()
    
    try:
        # Update statistics
        total_requests += 1
        last_request_time = datetime.now().isoformat()
        
        # Clean up old files in the background
        background_tasks.add_task(cleanup_old_files)
        
        # Generate speech
        filename = await tts_engine.generate_speech(
            text=request.text,
            engine=request.engine,
            lang=request.language,
            voice=request.voice,
            speed=request.speed,
            pitch=request.pitch,
            volume=request.volume
        )
        
        audio_url = f"/static/audio/{filename}"
        file_path = os.path.join("static/audio", filename)
        file_size = os.path.getsize(file_path)
        processing_time = time.time() - start_time
        

        text_preview = request.text[:50] + "..." if len(request.text) > 50 else request.text
        
        return TTSResponse(
            status="success",
            audio_url=audio_url,
            processing_time=round(processing_time, 2),
            text_preview=text_preview,
            file_size=file_size,
            created_at=datetime.now().isoformat(),
            engine=request.engine,
            voice=request.voice
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"TTS generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

@router.get("/voices", response_model=List[VoicesResponse])
async def get_voices(engine: Optional[str] = Query(None, description="Filter voices by engine")):
    """Get available voices for all engines"""
    try:
        voices_responses = []
        
        if not engine or engine == "edge-tts":
            edge_voices = await tts_engine.get_edge_voices()
            edge_voices_formatted = [
                Voice(
                    id=voice["ShortName"],
                    name=voice["DisplayName"],
                    locale=voice["Locale"],
                    gender=voice.get("Gender"),
                    sample_rate=voice.get("SampleRate")
                )
                for voice in edge_voices
            ]
            voices_responses.append(VoicesResponse(engine="edge-tts", voices=edge_voices_formatted))
        
        if not engine or engine == "pyttsx3":
            pyttsx3_voices = tts_engine.get_pyttsx3_voices()
            pyttsx3_voices_formatted = [
                Voice(
                    id=voice["id"],
                    name=voice["name"],
                    locale=None
                )
                for voice in pyttsx3_voices
            ]
            voices_responses.append(VoicesResponse(engine="pyttsx3", voices=pyttsx3_voices_formatted))
        
        if not engine or engine == "gtts":
            gtts_voices = [
                Voice(id="en", name="English", locale="en"),
                Voice(id="fr", name="French", locale="fr"),
                Voice(id="es", name="Spanish", locale="es"),
                Voice(id="de", name="German", locale="de"),
                Voice(id="it", name="Italian", locale="it"),
                Voice(id="ja", name="Japanese", locale="ja"),
                Voice(id="zh-CN", name="Chinese (Simplified)", locale="zh-CN"),
            ]
            voices_responses.append(VoicesResponse(engine="gtts", voices=gtts_voices))
        
        return voices_responses
    except Exception as e:
        logger.error(f"Failed to get voices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get voices: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with detailed statistics"""
    global total_requests, last_request_time, start_time
    
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="ok",
        message="TTS service is running",
        uptime=round(uptime, 2),
        total_requests=total_requests,
        last_request=last_request_time
    )