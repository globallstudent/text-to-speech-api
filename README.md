# Text-to-Speech API

A powerful and flexible Text-to-Speech (TTS) API built with FastAPI, supporting multiple TTS engines and voice customization options. This project provides both a REST API and a modern web interface for converting text to speech.

![Text-to-Speech API](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## Features

- 🎙️ Multiple TTS Engines Support:
  - Google TTS (gTTS)
  - Microsoft Edge TTS
  - pyttsx3 (Offline)
- 🎚️ Voice Customization:
  - Speed control (0.5x - 2.0x)
  - Pitch adjustment (0.5x - 2.0x)
  - Volume control (0.0x - 2.0x)
- 🌐 Modern Web Interface:
  - Responsive design
  - Real-time voice preview
  - Easy file download
- 🔧 API Features:
  - RESTful endpoints
  - Voice selection
  - File management
  - Health monitoring

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/globallstudent/text-to-speech-api.git
cd text-to-speech-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The web interface will be available at: http://localhost:8000

### API Endpoints

1. **Convert Text to Speech**
   - **Endpoint**: `POST /api/tts`
   - **Request Body**:
     ```json
     {
       "text": "Hello, world!",
       "engine": "edge-tts",
       "language": "en",
       "voice": "en-US-AriaNeural",
       "speed": 1.0,
       "pitch": 1.0,
       "volume": 1.0
     }
     ```
   - **Response**:
     ```json
     {
       "status": "success",
       "audio_url": "/static/audio/filename.mp3",
       "processing_time": 1.23,
       "text_preview": "Hello, world!",
       "file_size": 12345,
       "created_at": "2024-01-01T12:00:00Z",
       "engine": "edge-tts",
       "voice": "en-US-AriaNeural"
     }
     ```

2. **Get Available Voices**
   - **Endpoint**: `GET /api/tts/voices`
   - **Query Parameters**:
     - `engine` (optional): Filter voices by engine
   - **Response**:
     ```json
     [
       {
         "engine": "edge-tts",
         "voices": [
           {
             "id": "en-US-AriaNeural",
             "name": "Aria",
             "locale": "en-US",
             "gender": "Female",
             "sample_rate": 24000
           }
         ]
       }
     ]
     ```

3. **Health Check**
   - **Endpoint**: `GET /api/tts/health`
   - **Response**:
     ```json
     {
       "status": "ok",
       "message": "TTS service is running",
       "uptime": 3600.0,
       "total_requests": 100,
       "last_request": "2024-01-01T12:00:00Z"
     }
     ```

### Web Interface

The web interface provides an easy-to-use form for converting text to speech:

1. Enter your text in the text area
2. Select a TTS engine
3. Choose a voice
4. Adjust speed, pitch, and volume
5. Click "Convert to Speech"
6. Download the generated audio file

## Project Structure

```
text-to-speech-api/
├── app/
│   ├── main.py           # FastAPI application
│   ├── routers/
│   │   └── tts.py        # TTS API endpoints
│   └── tts_engine.py     # TTS engine implementation
├── static/
│   ├── audio/            # Generated audio files
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # Frontend JavaScript
│   └── index.html        # Web interface
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [gTTS](https://gtts.readthedocs.io/) - Google Text-to-Speech
- [Edge TTS](https://github.com/rany2/edge-tts) - Microsoft Edge TTS
- [pyttsx3](https://pyttsx3.readthedocs.io/) - Offline TTS engine

## Contact

- GitHub: [@globallstudent](https://github.com/globallstudent)
- Portfolio: [globalstudent.uz](https://globalstudent.uz)