import os
import traceback
import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# =========================
# IMPORT MODULES
# =========================
from audio_processing import transcribe_audio, extract_audio_features
from nlp_analysis import analyze_grammar, analyze_sentiment, analyze_relevance
from scoring import calculate_scores

# =========================
# FLASK CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "../frontend"),
    static_url_path=""
)
CORS(app)

# =========================
# TEMP + LOG FILE
# =========================
TEMP_DIR = os.path.join(BASE_DIR, 'temp_recordings')
LOG_FILE = os.path.join(BASE_DIR, "results_log.json")

os.makedirs(TEMP_DIR, exist_ok=True)

# =========================
# QUESTIONS
# =========================
INTERVIEW_QUESTIONS = [
# ===== BEHAVIOURAL =====
{"id": 1, "category": "Behavioural", "text": "Tell me about yourself."},
{"id": 2, "category": "Behavioural", "text": "Describe a challenging project you worked on."},
{"id": 3, "category": "Behavioural", "text": "Tell me about a time you failed."},
{"id": 4, "category": "Behavioural", "text": "Describe a time you handled pressure."},
{"id": 5, "category": "Behavioural", "text": "Tell me about a conflict in your team."},
{"id": 6, "category": "Behavioural", "text": "Describe a time you showed leadership."},
{"id": 7, "category": "Behavioural", "text": "Tell me about a time you met a deadline."},
{"id": 8, "category": "Behavioural", "text": "Describe a mistake you made."},
{"id": 9, "category": "Behavioural", "text": "Tell me about a time you learned something new quickly."},
{"id": 10, "category": "Behavioural", "text": "Describe a time you helped a teammate."},
{"id": 11, "category": "Behavioural", "text": "Tell me about a time you handled criticism."},
{"id": 12, "category": "Behavioural", "text": "Describe a time you went above expectations."},
{"id": 13, "category": "Behavioural", "text": "Tell me about a time you solved a problem creatively."},
{"id": 14, "category": "Behavioural", "text": "Describe a time you worked under ambiguity."},
{"id": 15, "category": "Behavioural", "text": "Tell me about a time you disagreed with your team."},

# ===== SITUATIONAL =====
{"id": 16, "category": "Situational", "text": "How would you handle tight deadlines?"},
{"id": 17, "category": "Situational", "text": "How would you deal with a difficult teammate?"},
{"id": 18, "category": "Situational", "text": "What would you do if you missed a deadline?"},
{"id": 19, "category": "Situational", "text": "How would you handle multiple tasks?"},
{"id": 20, "category": "Situational", "text": "What would you do if your idea was rejected?"},
{"id": 21, "category": "Situational", "text": "How would you manage conflict in a team?"},
{"id": 22, "category": "Situational", "text": "What would you do if you didn’t understand a task?"},
{"id": 23, "category": "Situational", "text": "How would you prioritize tasks?"},
{"id": 24, "category": "Situational", "text": "What would you do under pressure?"},
{"id": 25, "category": "Situational", "text": "How would you explain something technical to a non-technical person?"},
{"id": 26, "category": "Situational", "text": "What would you do if a project failed?"},
{"id": 27, "category": "Situational", "text": "How would you react to feedback?"},
{"id": 28, "category": "Situational", "text": "What would you do if you had no guidance?"},
{"id": 29, "category": "Situational", "text": "How would you handle unrealistic expectations?"},
{"id": 30, "category": "Situational", "text": "What would you do if your team disagrees with you?"},

# ===== HR QUESTIONS =====
{"id": 31, "category": "HR", "text": "Why should we hire you?"},
{"id": 32, "category": "HR", "text": "What are your strengths?"},
{"id": 33, "category": "HR", "text": "What are your weaknesses?"},
{"id": 34, "category": "HR", "text": "Where do you see yourself in 5 years?"},
{"id": 35, "category": "HR", "text": "Why do you want to join our company?"},
{"id": 36, "category": "HR", "text": "What motivates you?"},
{"id": 37, "category": "HR", "text": "What are your career goals?"},
{"id": 38, "category": "HR", "text": "Are you willing to relocate?"},
{"id": 39, "category": "HR", "text": "What makes you different from others?"},
{"id": 40, "category": "HR", "text": "What is your biggest achievement?"},
{"id": 41, "category": "HR", "text": "How do you handle stress?"},
{"id": 42, "category": "HR", "text": "What are your hobbies?"},
{"id": 43, "category": "HR", "text": "What are your salary expectations?"},
{"id": 44, "category": "HR", "text": "Why did you choose this field?"},
{"id": 45, "category": "HR", "text": "What is your dream company?"},

# ===== TECHNICAL / GENERAL =====
{"id": 46, "category": "Technical", "text": "Explain OOP concepts."},
{"id": 47, "category": "Technical", "text": "What is polymorphism?"},
{"id": 48, "category": "Technical", "text": "Explain inheritance."},
{"id": 49, "category": "Technical", "text": "What is encapsulation?"},
{"id": 50, "category": "Technical", "text": "Difference between array and linked list."},
{"id": 51, "category": "Technical", "text": "Explain database normalization."},
{"id": 52, "category": "Technical", "text": "What is SQL?"},
{"id": 53, "category": "Technical", "text": "Explain joins in SQL."},
{"id": 54, "category": "Technical", "text": "What is machine learning?"},
{"id": 55, "category": "Technical", "text": "Difference between AI and ML."},
{"id": 56, "category": "Technical", "text": "Explain REST API."},
{"id": 57, "category": "Technical", "text": "What is Git?"},
{"id": 58, "category": "Technical", "text": "What is a stack and queue?"},
{"id": 59, "category": "Technical", "text": "Explain recursion."},
{"id": 60, "category": "Technical", "text": "What is cloud computing?"},

# ===== EXTRA (ADVANCED + MIXED) =====
{"id": 61, "category": "Mixed", "text": "How do you handle failure?"},
{"id": 62, "category": "Mixed", "text": "What is your leadership style?"},
{"id": 63, "category": "Mixed", "text": "How do you stay updated with technology?"},
{"id": 64, "category": "Mixed", "text": "Describe your ideal work environment."},
{"id": 65, "category": "Mixed", "text": "How do you handle feedback?"},
{"id": 66, "category": "Mixed", "text": "What challenges are you looking for?"},
{"id": 67, "category": "Mixed", "text": "How do you manage time?"},
{"id": 68, "category": "Mixed", "text": "What inspires you?"},
{"id": 69, "category": "Mixed", "text": "How do you learn new skills?"},
{"id": 70, "category": "Mixed", "text": "What is your biggest weakness?"},
{"id": 71, "category": "Mixed", "text": "What is your biggest strength?"},
{"id": 72, "category": "Mixed", "text": "Describe a leadership experience."},
{"id": 73, "category": "Mixed", "text": "What does teamwork mean to you?"},
{"id": 74, "category": "Mixed", "text": "How do you handle criticism?"},
{"id": 75, "category": "Mixed", "text": "Describe a stressful situation."},

# ===== FINAL SET =====
{"id": 76, "category": "Behavioural", "text": "Tell me about a time you improved a process."},
{"id": 77, "category": "Behavioural", "text": "Describe a time you worked independently."},
{"id": 78, "category": "Behavioural", "text": "Tell me about a time you failed and recovered."},
{"id": 79, "category": "Situational", "text": "What would you do if your manager is wrong?"},
{"id": 80, "category": "Situational", "text": "How would you deal with tight deadlines?"},
{"id": 81, "category": "HR", "text": "Why do you want this job?"},
{"id": 82, "category": "HR", "text": "What are your expectations from us?"},
{"id": 83, "category": "Technical", "text": "Explain data structures."},
{"id": 84, "category": "Technical", "text": "What is API?"},
{"id": 85, "category": "Technical", "text": "Explain version control."},
{"id": 86, "category": "Mixed", "text": "What are your short-term goals?"},
{"id": 87, "category": "Mixed", "text": "What are your long-term goals?"},
{"id": 88, "category": "Mixed", "text": "Describe your decision-making process."},
{"id": 89, "category": "Mixed", "text": "What makes a good team?"},
{"id": 90, "category": "Mixed", "text": "How do you define success?"},
{"id": 91, "category": "Mixed", "text": "How do you stay productive?"},
{"id": 92, "category": "Mixed", "text": "What is your work ethic?"},
{"id": 93, "category": "Mixed", "text": "Describe your communication style."},
{"id": 94, "category": "Mixed", "text": "How do you solve problems?"},
{"id": 95, "category": "Mixed", "text": "What challenges have you overcome?"},
{"id": 96, "category": "Mixed", "text": "What is your proudest moment?"},
{"id": 97, "category": "Mixed", "text": "What do you value most in a job?"},
{"id": 98, "category": "Mixed", "text": "How do you handle change?"},
{"id": 99, "category": "Mixed", "text": "How do you approach learning?"},
{"id": 100, "category": "Mixed", "text": "What makes you unique?"}
]

# =========================
# FRONTEND ROUTES
# =========================
@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return app.send_static_file(path)

# =========================
# API ROUTES
# =========================
@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify(random.choice(INTERVIEW_QUESTIONS))


@app.route("/api/process_audio", methods=["POST"])
def process_audio_route():

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    question_text = request.form.get("question", "Tell me about yourself.")

    filename = f"recording_{random.randint(1000,9999)}.webm"
    filepath = os.path.join(TEMP_DIR, filename)

    file.save(filepath)

    try:
        # =========================
        # TRANSCRIPTION
        # =========================
        transcript = transcribe_audio(filepath)

        if (
            not transcript.strip()
            or "transcription failed" in transcript.lower()
            or "no speech" in transcript.lower()
        ):
            return jsonify({
                "error": "No valid speech detected. Please speak clearly and try again."
            }), 400

        # =========================
        # AUDIO FEATURES
        # =========================
        audio_features = extract_audio_features(filepath)

        # =========================
        # NLP ANALYSIS
        # =========================
        grammar_res = analyze_grammar(transcript)
        sentiment_res = analyze_sentiment(transcript)
        relevance_score = analyze_relevance(question_text, transcript)

        nlp_metrics = {
            "text_length": len(transcript.split()),
            "grammar_errors": grammar_res.get("num_errors", 0),
            "sentiment": sentiment_res,
            "relevance_score": relevance_score
        }

        # =========================
        # SCORING
        # =========================
        results = calculate_scores(audio_features, nlp_metrics)

        # =========================
        # 🔥 SAVE DATA FOR PLOTS
        # =========================
        entry = {
            "confidence": results["scores"]["confidence"],
            "fluency": results["scores"]["fluency"],
            "grammar": results["scores"]["grammar"],
            "relevance": results["scores"]["relevance"],
            "pitch": audio_features.get("pitchVariation", 0),
            "pauses": audio_features.get("numPauses", 0),
            "energy": audio_features.get("energy", 0),
            "duration": audio_features.get("durationSec", 0)
        }

        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    data = json.load(f)
            except:
                data = []
        else:
            data = []

        data.append(entry)

        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # =========================
        # RESPONSE
        # =========================
        return jsonify({
            "message": "Audio processed successfully",
            "transcript": transcript,
            "scores": results.get("scores", {}),
            "feedback": results.get("feedback", {})
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Processing failed: {str(e)}"
        }), 500

    finally:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)