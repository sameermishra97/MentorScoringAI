# helper_functions.py

import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def get_top_keywords(text: str, n: int = 5):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = ["this","that","with","from","about","they","have","your","will","then","been","their"]
    filtered = [w for w in words if w not in stopwords]
    freq = Counter(filtered)
    return [w for w,_ in freq.most_common(n)]

def get_rating(overall: float) -> str:
    if overall >= 85:
        return "🌟 Excellent Mentor"
    elif overall >= 70:
        return "✅ Good Mentor"
    elif overall >= 50:
        return "⚙️ Average Mentor"
    else:
        return "🔁 Needs Improvement"

def generate_insights(scores: dict) -> str:
    if scores["Clarity"] < 60:
        return "Speech clarity can be improved by shortening sentences and simplifying wording."
    elif scores["Tone"] < 60:
        return "Tone is flat — use more enthusiasm to keep students engaged."
    elif scores["Engagement"] < 60:
        return "Try adding interactive phrases such as 'imagine', 'let’s', or 'think about'."
    elif scores["Depth"] < 60:
        return "The explanation could include more examples or technical references."
    else:
        return "Excellent clarity and teaching engagement!"

def radar_chart(scores: dict):
    labels = ["Clarity", "Tone", "Depth", "Engagement"]
    values = [scores[l] for l in labels]
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels)+1)

    fig = plt.figure(figsize=(5,5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title("Mentor Evaluation Radar Chart")
    plt.show()
