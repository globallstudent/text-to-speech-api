# app/tts_engine.py
import os
import uuid
from gtts import gTTS
import pyttsx3

class TTSEngine:
    def __init__(self, engine_type="gtts", output_dir="static/audio"):
        self.engine_type = engine_type
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize offline engine if needed
        if self.engine_type == "pyttsx3":
            self.engine = pyttsx3.init()
    
    def generate_speech(self, text, lang="en", voice=None, speed=1.0):
        """Generate speech from text and return the file path"""
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        if self.engine_type == "gtts":
            # Using Google's TTS service (requires internet)
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(filepath)
        
        elif self.engine_type == "pyttsx3":
            # Using offline pyttsx3
            if voice:
                voices = self.engine.getProperty('voices')
                for v in voices:
                    if voice in v.id:
                        self.engine.setProperty('voice', v.id)
                        break
            
            # Set speed rate
            self.engine.setProperty('rate', 200 * speed)
            
            # Save to file
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
        
        return filename