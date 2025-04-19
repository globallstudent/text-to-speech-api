from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech", example="Hello, world!")
    engine: str = Field("gtts", description="TTS engine to use", example="gtts")
    language: str = Field("en", description="Language code", example="en")
    voice: Optional[str] = Field(None, description="Voice ID or name", example="en-US-AriaNeural")
    speed: float = Field(1.0, description="Speech speed multiplier", example=1.0, ge=0.5, le=2.0)
    pitch: float = Field(1.0, description="Voice pitch multiplier", example=1.0, ge=0.5, le=2.0)
    volume: float = Field(1.0, description="Voice volume multiplier", example=1.0, ge=0.0, le=2.0)

    @field_validator('text')
    def validate_text_length(cls, v):
        if len(v) > 5000:
            raise ValueError('Text length must be less than 5000 characters')
        return v

class TTSResponse(BaseModel):
    status: str
    audio_url: str
    processing_time: float
    text_preview: str
    file_size: int
    created_at: str
    engine: str
    voice: Optional[str] = None

class Voice(BaseModel):
    id: str
    name: str
    locale: Optional[str] = None
    gender: Optional[str] = None
    sample_rate: Optional[int] = None

class VoicesResponse(BaseModel):
    engine: str
    voices: List[Voice]

class HealthResponse(BaseModel):
    status: str
    message: str
    uptime: float
    total_requests: int
    last_request: Optional[str] = None