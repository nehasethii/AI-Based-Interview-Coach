import librosa
import numpy as np
import whisper
import os

# =========================
# LOAD MODEL ONCE
# =========================
print("Loading Whisper Model...")
try:
    model = whisper.load_model("tiny")  # tiny = fast, base = better accuracy
except Exception as e:
    print("Error loading Whisper:", e)
    model = None


# =========================
# TRANSCRIPTION
# =========================
def transcribe_audio(filepath):
    try:
        if model is None:
            raise Exception("Whisper model not loaded")

        result = model.transcribe(filepath)
        text = result.get("text", "").strip()

        return text if text else "No speech detected"

    except Exception as e:
        print("Transcription Error:", e)
        return "Transcription failed"


# =========================
# AUDIO FEATURES
# =========================
def extract_audio_features(filepath):
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError("Audio file not found")

        # Load audio safely
        y, sr = librosa.load(filepath, sr=16000)

        if len(y) == 0:
            raise ValueError("Empty audio signal")

        # =========================
        # DURATION
        # =========================
        total_duration = librosa.get_duration(y=y, sr=sr)

        # =========================
        # SILENCE / PAUSE DETECTION
        # =========================
        intervals = librosa.effects.split(y, top_db=25)  # slightly more sensitive

        speaking_duration = sum(
            (end - start) / sr for start, end in intervals
        )

        pause_duration = max(0, total_duration - speaking_duration)
        num_pauses = max(0, len(intervals) - 1)

        # =========================
        # SPEAKING RATE (NEW 🔥)
        # =========================
        words_estimate = len(y) / sr / 0.4  # rough words/sec estimate
        speaking_rate = round(words_estimate / total_duration, 2) if total_duration > 0 else 0

        # =========================
        # ENERGY (CONFIDENCE PROXY 🔥)
        # =========================
        rms = librosa.feature.rms(y=y)
        energy = float(np.mean(rms))

        # =========================
        # PITCH (SIMPLIFIED + FAST)
        # =========================
        try:
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_vals = []

            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if 50 < pitch < 500:
                    pitch_vals.append(pitch)

            pitch_variation = float(np.std(pitch_vals)) if pitch_vals else 0.0
        except:
            pitch_variation = 0.0

        return {
            "durationSec": round(total_duration, 2),
            "speakingDurationSec": round(speaking_duration, 2),
            "pauseDurationSec": round(pause_duration, 2),
            "numPauses": int(num_pauses),
            "pitchVariation": round(pitch_variation, 2),
            "energy": round(energy, 4),
            "speakingRate": speaking_rate
        }

    except Exception as e:
        print("Audio Feature Error:", e)

        # Safe fallback (VERY IMPORTANT)
        return {
            "durationSec": 0,
            "speakingDurationSec": 0,
            "pauseDurationSec": 0,
            "numPauses": 0,
            "pitchVariation": 0,
            "energy": 0,
            "speakingRate": 0
        }