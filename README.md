# Text-to-Speech API

A simple and practical Text-to-Speech API built with FastAPI. It provides a straightforward way to convert text to speech using different engines and includes a basic web interface.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## What it does

- Converts text to speech using different engines:
  - Google TTS (gTTS)
  - Microsoft Edge TTS
  - pyttsx3 (works offline)
- Lets you adjust voice settings:
  - Speed
  - Pitch
  - Volume
- Provides a simple web interface
- Offers basic API endpoints

## Getting Started

### What you need

- Python 3.8 or newer
- pip
- A virtual environment (recommended)

### Setup

1. Get the code:
```bash
git clone https://github.com/globallstudent/text-to-speech-api.git
cd text-to-speech-api
```

2. Set up your environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

## How to use it

### Start the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000 to use the web interface.

### API basics

1. **Convert text to speech**
   - `POST /api/tts`
   - Example request:
     ```json
     {
       "text": "Hello",
       "engine": "edge-tts",
       "voice": "en-US-AriaNeural"
     }
     ```

2. **Get available voices**
   - `GET /api/tts/voices`
   - Optional: `?engine=edge-tts`

3. **Check server status**
   - `GET /api/tts/health`

### Web interface

The web interface is simple to use:
1. Type your text
2. Pick an engine and voice
3. Adjust settings if needed
4. Click convert
5. Download the audio if you want

## Project Structure

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

Feel free to help improve this project. Just:
1. Fork the repo
2. Make your changes
3. Submit a pull request

## Thanks

This project uses:
- [FastAPI](https://fastapi.tiangolo.com/)
- [gTTS](https://gtts.readthedocs.io/)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [pyttsx3](https://pyttsx3.readthedocs.io/)

## License

MIT License - see [LICENSE](LICENSE)

## Contact

- GitHub: [@globallstudent](https://github.com/globallstudent)
- Website: [globalstudent.uz](https://globalstudent.uz)