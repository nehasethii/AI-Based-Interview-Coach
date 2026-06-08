import json
import matplotlib.pyplot as plt

# Load data
with open("backend/results_log.json", "r") as f:
    data = json.load(f)

# Extract values
confidence = [d["confidence"] for d in data]
fluency = [d["fluency"] for d in data]
grammar = [d["grammar"] for d in data]
relevance = [d["relevance"] for d in data]

pitch = [d["pitch"] for d in data]
pauses = [d["pauses"] for d in data]
energy = [d["energy"] for d in data]

sessions = list(range(1, len(data)+1))

# =========================
# 1. SCORE TREND
# =========================
plt.figure()
plt.plot(sessions, confidence, label="Confidence")
plt.plot(sessions, fluency, label="Fluency")
plt.plot(sessions, grammar, label="Grammar")
plt.plot(sessions, relevance, label="Relevance")
plt.xlabel("Session")
plt.ylabel("Score")
plt.title("Performance Over Multiple Responses")
plt.legend()
plt.show()

# =========================
# 2. SCORE DISTRIBUTION
# =========================
avg_scores = [
    sum(confidence)/len(confidence),
    sum(fluency)/len(fluency),
    sum(grammar)/len(grammar),
    sum(relevance)/len(relevance)
]

labels = ["Confidence", "Fluency", "Grammar", "Relevance"]

plt.figure()
plt.bar(labels, avg_scores)
plt.title("Average Performance Scores")
plt.ylabel("Score")
plt.show()

# =========================
# 3. PITCH VARIATION
# =========================
plt.figure()
plt.plot(sessions, pitch)
plt.title("Pitch Variation Across Responses")
plt.xlabel("Session")
plt.ylabel("Pitch Variation")
plt.show()

# =========================
# 4. PAUSE ANALYSIS
# =========================
plt.figure()
plt.plot(sessions, pauses)
plt.title("Number of Pauses per Response")
plt.xlabel("Session")
plt.ylabel("Pauses")
plt.show()

# =========================
# 5. ENERGY ANALYSIS
# =========================
plt.figure()
plt.plot(sessions, energy)
plt.title("Speech Energy Levels")
plt.xlabel("Session")
plt.ylabel("Energy")
plt.show()