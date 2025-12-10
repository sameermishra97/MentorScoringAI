# mentor_scoring_ai.py

from transformers import pipeline
import textstat
from empath import Empath

# Load models once
sentiment_model = pipeline("sentiment-analysis")
lexicon = Empath()

def mentor_scoring_ai(text: str) -> dict:
    """
    Core Mentor Scoring AI logic.
    Evaluates text on Clarity, Tone, Depth, Engagement, and returns Overall Score.
    """
    text = text.strip()
    if not text:
        return {"Error": "Please provide some input text."}

    # --- Clarity ---
    try:
        readability = textstat.flesch_reading_ease(text)
    except Exception:
        readability = 60.0
    clarity = min(max(readability, 0), 100)

    # --- Tone / Emotion ---
    sentiment = sentiment_model(text[:512])[0]
    tone = round(sentiment['score'] * 100, 2)

    # --- Knowledge Depth ---
    topics = lexicon.analyze(text)
    academic_terms = topics.get('education', 0) + topics.get('science', 0) + topics.get('technology', 0)
    depth = min(academic_terms * 10, 100)

    # --- Engagement ---
    engagement_keywords = ['imagine', 'try', 'let’s', 'you can', 'think about', 'practice', 'together', 'consider']
    hits = sum(text.lower().count(k) for k in engagement_keywords)
    engagement = min(hits * 15, 100)

    # --- Weighted Overall ---
    overall = 0.3 * clarity + 0.3 * tone + 0.2 * depth + 0.2 * engagement

    scores = {
        "Clarity": round(clarity, 2),
        "Tone": round(tone, 2),
        "Depth": round(depth, 2),
        "Engagement": round(engagement, 2),
        "Overall Mentor Score": round(overall, 2)
    }
    return scores
