def calculate_scores(audio_features, nlp_metrics):
    """
    Robust + stable scoring with better normalization and dynamic feedback
    """

    # =========================
    # SAFE EXTRACTION
    # =========================
    duration = max(1.0, float(audio_features.get("durationSec", 1.0)))
    num_words = float(nlp_metrics.get("text_length", 0))

    pause_duration = float(audio_features.get("pauseDurationSec", 0.0))
    num_pauses = int(audio_features.get("numPauses", 0))
    pitch_variation = float(audio_features.get("pitchVariation", 0.0))
    energy = float(audio_features.get("energy", 0.0))
    speaking_rate_feature = float(audio_features.get("speakingRate", 0.0))

    grammar_errors = int(nlp_metrics.get("grammar_errors", 0))
    relevance_raw = float(nlp_metrics.get("relevance_score", 0.0))
    sentiment = nlp_metrics.get("sentiment", {})

    polarity = sentiment.get("polarity", 0)

    # =========================
    # FLUENCY (FIXED 🔥)
    # =========================
    wpm = (num_words / duration) * 60.0 if duration > 0 else 0
    pause_ratio = pause_duration / duration

    fluency = 100.0

    # softer penalties (avoid 0 score issue)
    if wpm < 90:
        fluency -= min(25, (90 - wpm) * 0.3)
    elif wpm > 180:
        fluency -= min(20, (wpm - 180) * 0.3)

    if pause_ratio > 0.35:
        fluency -= min(30, (pause_ratio - 0.35) * 100)

    if num_pauses > 8:
        fluency -= 10

    fluency = max(10.0, min(100.0, fluency))  # 🔥 prevent 0 lock

    # =========================
    # GRAMMAR
    # =========================
    grammar = max(0, 100 - (grammar_errors * 10))

    # =========================
    # RELEVANCE (FIXED SCALING)
    # =========================
    relevance = max(0.0, min(100.0, relevance_raw * 100))

    # =========================
    # CONFIDENCE (STABILIZED 🔥)
    # =========================
    sentiment_bonus = polarity * 15  # smoother

    # Pitch
    if pitch_variation > 30:
        pitch_bonus = 10
    elif pitch_variation > 15:
        pitch_bonus = 5
    elif pitch_variation < 5:
        pitch_bonus = -8
    else:
        pitch_bonus = 0

    # Energy
    if energy > 0.05:
        energy_bonus = 10
    elif energy > 0.02:
        energy_bonus = 5
    else:
        energy_bonus = -8

    # Speaking rate consistency
    if 1.5 <= speaking_rate_feature <= 3.5:
        rate_bonus = 5
    else:
        rate_bonus = -3

    confidence = (
        fluency * 0.45
        + relevance * 0.25
        + sentiment_bonus
        + pitch_bonus
        + energy_bonus
        + rate_bonus
    )

    confidence = max(10.0, min(100.0, confidence))  # 🔥 avoid 0

    # =========================
    # DYNAMIC FEEDBACK (FIXED 🔥)
    # =========================
    strengths = []
    improvements = []

    # Pace
    if 110 <= wpm <= 160:
        strengths.append("Good speaking pace.")
    elif wpm < 110:
        improvements.append("Try speaking slightly faster.")
    else:
        improvements.append("You are speaking too fast. Slow down slightly.")

    # Pauses
    if pause_ratio < 0.2:
        strengths.append("Smooth delivery with minimal pauses.")
    elif pause_ratio > 0.4:
        improvements.append("Reduce long pauses to improve fluency.")

    # Energy
    if energy > 0.04:
        strengths.append("Good vocal energy.")
    else:
        improvements.append("Add more energy and clarity while speaking.")

    # Grammar
    if grammar > 80:
        strengths.append("Strong grammar usage.")
    else:
        improvements.append("Improve sentence structure.")

    # Relevance
    if relevance > 70:
        strengths.append("Answer is relevant to the question.")
    elif relevance < 40:
        improvements.append("Use STAR method for better relevance.")

    # Confidence cues
    if confidence > 70:
        strengths.append("You sound confident.")
    else:
        improvements.append("Try to sound more confident and assertive.")

    # fallback
    if not strengths:
        strengths.append("Good effort, keep practicing.")

    if not improvements:
        improvements.append("Great performance overall.")

    return {
        "scores": {
            "confidence": int(confidence),
            "fluency": int(fluency),
            "grammar": int(grammar),
            "relevance": int(relevance)
        },
        "feedback": {
            "strengths": strengths[:3],
            "improvements": improvements[:3]
        }
    }