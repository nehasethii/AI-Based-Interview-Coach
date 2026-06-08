# 🎤 AI-Based Offline Interview Coach

An intelligent interview preparation platform that analyzes spoken interview responses and provides automated feedback on communication quality, confidence, fluency, grammar, sentiment, and answer relevance.

Unlike traditional cloud-based interview tools, this system performs all processing locally on the user's machine, ensuring complete privacy while delivering AI-powered insights through speech processing and Natural Language Processing (NLP) techniques.

---

## 🚀 Key Features

### 🎙 Speech-to-Text Transcription

Converts spoken interview responses into text using OpenAI Whisper for accurate offline transcription.

### 📊 Communication Analysis

Evaluates important speaking metrics including:

* Speaking Rate (Words Per Minute)
* Pause Duration Analysis
* Fluency Assessment
* Confidence Indicators

### 🧠 NLP-Powered Feedback

Generates detailed feedback using multiple NLP models:

* Grammar Analysis using LanguageTool
* Sentiment Analysis using DistilBERT
* Semantic Answer Relevance using Sentence-BERT
* Structured Interview Performance Evaluation

### 🔒 Privacy-First Architecture

All processing is performed locally.

* No cloud APIs
* No external data sharing
* No interview recordings uploaded
* Fully offline operation after model download

### 📈 Interactive Feedback Dashboard

Provides visual performance insights through:

* Confidence Score
* Fluency Score
* Grammar Score
* Relevance Score
* Overall Interview Performance Summary

---

## 🏗 System Workflow

```text
Interview Response
        ↓
Audio Recording
        ↓
Whisper Speech-to-Text
        ↓
Audio Feature Extraction
        ↓
NLP Analysis
        ↓
Performance Scoring
        ↓
Feedback Dashboard
```

---

## 🛠 Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* MediaRecorder API

### Backend

* Flask

### Speech Processing

* OpenAI Whisper
* Librosa

### Natural Language Processing

* DistilBERT
* Sentence-BERT
* LanguageTool

### Machine Learning

* Transformers
* Sentence Transformers

---

## ⚙️ Installation

### Prerequisites

* Python 3.9+
* Java (Required for LanguageTool)
* FFmpeg (Required by Whisper)

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run Backend

```bash
python app.py
```

### Run Frontend

```bash
cd frontend
python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

---

## 🔐 Privacy

This project is designed with a privacy-first approach. Audio recordings, transcripts, and evaluation results remain on the user's device and are never transmitted to external servers.

---

## 🎯 Future Enhancements

* Personalized interview question generation
* Domain-specific interview preparation
* Real-time speech coaching
* Multilingual interview analysis
* AI-generated improvement suggestions

---

## 👩‍💻 Author

**Neha Sethi**

B.Tech Information Technology
Machine Learning • NLP • Software Development

---

> Helping candidates practice smarter through AI-powered interview feedback.
