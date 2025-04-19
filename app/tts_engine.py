import os
import uuid
import logging
from gtts import gTTS
import pyttsx3
import asyncio
import edge_tts

logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self, engine_type="gtts", output_dir="static/audio"):
        self.engine_type = engine_type
        self.output_dir = output_dir
        
        os.makedirs(self.output_dir, exist_ok=True)
        

        if self.engine_type == "pyttsx3":
            self.engine = pyttsx3.init()
    
    async def generate_speech(self, text, engine="gtts", lang="en", voice=None, speed=1.0, pitch=1.0, volume=1.0):
        """Generate speech from text and return the file path"""
        try:
            # Generate a unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.output_dir, filename)
            
            if engine == "gtts":
                # Using Google's TTS service (requires internet)
                logger.info(f"Generating speech with gTTS: {text[:50]}...")
                tts = gTTS(text=text, lang=lang, slow=False)
                tts.save(filepath)
            
            elif engine == "pyttsx3":
                # Using offline pyttsx3
                logger.info(f"Generating speech with pyttsx3: {text[:50]}...")
                if voice:
                    voices = self.engine.getProperty('voices')
                    for v in voices:
                        if voice in v.id:
                            self.engine.setProperty('voice', v.id)
                            break
                
                # Set speed rate (default is 200, range is 50-500)
                self.engine.setProperty('rate', 200 * speed)
                
                # Set pitch (default is 1.0, range is 0.5-2.0)
                # Note: pyttsx3 doesn't directly support pitch, we adjust rate instead
                self.engine.setProperty('rate', int(200 * speed * pitch))
                
                # Set volume (default is 1.0, range is 0.0-1.0)
                self.engine.setProperty('volume', volume)
                
                # Save to file
                self.engine.save_to_file(text, filepath)
                self.engine.runAndWait()
            
            elif engine == "edge-tts":
                # Using Edge TTS (better quality)
                logger.info(f"Generating speech with Edge TTS: {text[:50]}...")
                voice = voice or "en-US-AriaNeural"
                
                # Create communicate object with rate (speed) and volume
                communicate = edge_tts.Communicate(
                    text,
                    voice,
                    rate=f"{int((speed - 1) * 100)}%",  # Edge TTS uses percentage for rate
                    volume=f"{int((volume - 1) * 100)}%"  # Edge TTS uses percentage for volume
                )
                await communicate.save(filepath)
            
            else:
                raise ValueError(f"Unsupported engine: {engine}")
            
            return filename
            
        except Exception as e:
            logger.error(f"Speech generation failed: {str(e)}")
            raise
    
    async def get_edge_voices(self):
        """Get available Edge TTS voices"""
        try:
            voices = await edge_tts.list_voices()
            return voices
        except Exception as e:
            logger.error(f"Failed to get Edge TTS voices: {str(e)}")
            return []
    
    def get_pyttsx3_voices(self):
        """Get available pyttsx3 voices"""
        try:
            # Initialize pyttsx3 and get voices
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            voice_list = [
                {"id": voice.id, "name": voice.name, "languages": getattr(voice, 'languages', [])}
                for voice in voices
            ]
            
            return voice_list
        except Exception as e:
            logger.error(f"Failed to get pyttsx3 voices: {str(e)}")
            return []