import language_tool_python
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

print("Loading NLP Models...")

# =========================
# GRAMMAR TOOL
# =========================
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    print(f"LanguageTool failed (Java missing): {e}")
    tool = None

# =========================
# SENTIMENT MODEL
# =========================
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
except Exception as e:
    print(f"Sentiment model failed: {e}")
    sentiment_analyzer = None

# =========================
# SBERT MODEL
# =========================
try:
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"SBERT failed: {e}")
    sbert_model = None


# =========================
# GRAMMAR
# =========================
def analyze_grammar(text):
    if tool is None or not text.strip():
        return {"num_errors": 0, "errors": []}

    try:
        matches = tool.check(text)

        errors = [
            {"message": m.message, "context": m.context}
            for m in matches
        ]

        return {
            "num_errors": len(errors),
            "errors": errors
        }

    except Exception as e:
        print("Grammar error:", e)
        return {"num_errors": 0, "errors": []}


# =========================
# SENTIMENT (FIXED FORMAT 🔥)
# =========================
def analyze_sentiment(text):
    if not text.strip() or sentiment_analyzer is None:
        return {"polarity": 0.0, "label": "NEUTRAL"}

    try:
        result = sentiment_analyzer(text[:512])[0]

        label = result["label"]
        score = result["score"]

        # Convert to polarity (-1 to 1)
        polarity = score if label == "POSITIVE" else -score

        return {
            "polarity": round(polarity, 2),
            "label": label
        }

    except Exception as e:
        print("Sentiment error:", e)
        return {"polarity": 0.0, "label": "NEUTRAL"}


# =========================
# RELEVANCE (OPTIMIZED 🔥)
# =========================
def analyze_relevance(question, answer):
    if not answer.strip() or not question.strip() or sbert_model is None:
        return 0.0

    try:
        embeddings = sbert_model.encode(
            [question, answer],
            convert_to_tensor=True
        )

        sim_score = util.cos_sim(embeddings[0], embeddings[1]).item()

        return max(0.0, round(sim_score, 3))

    except Exception as e:
        print("Relevance error:", e)
        return 0.0