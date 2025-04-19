import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tts

# Create directories if they don't exist
os.makedirs("static/audio", exist_ok=True)

app = FastAPI(
    title="TTS Web API",
    description="A Text-to-Speech API with web interface",
    version="1.0.0"
)

# CORS settings for local development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tts.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="static", html=True), name="site")