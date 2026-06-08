# AI-Based Offline Interview Coach

An intelligent system designed to help users practice interview responses and receive automated feedback on their communication skills. 

Unlike cloud-based interview platforms, this system processes data entirely offline on the user’s machine, ensuring privacy and accessibility. It utilizes NLP and Machine Learning for speech-to-text, audio feature extraction, and text analysis.

## Features
- **Offline AI Analysis**: Audio is processed privately on your machine using local models.
- **Speech-to-Text**: High-accuracy transcription using OpenAI Whisper.
- **Audio Metrics**: Evaluates speaking pace (WPM) and pause durations using Librosa.
- **NLP Analysis**: Grammar checks (LanguageTool), Sentiment Analysis (DistilBERT), and Answer Relevance (Sentence-BERT).
- **Rich Feedback Dashboard**: BeautifulUI that visualizes Confidence, Fluency, Grammar, and Relevance scores.

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9+ installed
- Java (Required for `language-tool-python` offline checks)
- ffmpeg installed (Required by Whisper for audio decoding)

*To install ffmpeg:*
- **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via winget `winget install ffmpeg`. Make sure it's added to your system PATH.
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt update && sudo apt install ffmpeg`

### 2. Install Dependencies
Open a terminal in the `backend` directory and install the python requirements. Note that model files will be downloaded automatically the first time you run the app.

```bash
cd AI-Based-Offline-Interview-Coach/backend
pip install -r requirements.txt
```

### 3. Run the Backend Server
Start the Flask API to serve requests and process audio files:
```bash
python app.py
```
*Note: On the first run, it will take some time to download the Whisper (`tiny`), DistilBERT, and MiniLM models. Once downloaded, they are cached locally for complete offline use.*

### 4. Run the Frontend
You can serve the frontend folder using a simple HTTP server (or just open `index.html` directly in your browser, but a server avoids strict CORS policies for microphone access):

Open a second terminal:
```bash
cd AI-Based-Offline-Interview-Coach/frontend
python -m http.server 8000
```
Then navigate to `http://localhost:8000` in your web browser.

---

## Privacy
Since everything runs locally, no audio data, transcripts, or scores are ever sent to an external cloud provider.

## Tech Stack
- **Frontend**: HTML5, CSS3, Javascript, MediaRecorder API
- **Backend API**: Flask
- **ML & Audio**: `whisper`, `librosa`, `transformers`, `sentence-transformers`, `language-tool-python`
