
# app.py

import gradio as gr
from mentor_scoring_ai import mentor_scoring_ai
from helper_functions import get_top_keywords, get_rating, generate_insights
import speech_recognition as sr

recognizer = sr.Recognizer()

def audio_to_text(audio_path: str):
    """Convert uploaded audio file to text"""
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        print("Audio processing error:", e)
        return ""

def mentor_scoring_interface(text, audio_file):
    # Optional: convert audio
    if audio_file is not None:
        text += "\n" + audio_to_text(audio_file.name)
    
    scores = mentor_scoring_ai(text)
    if "Error" in scores:
        return "⚠️ Please provide text or upload audio."

    rating = get_rating(scores["Overall Mentor Score"])
    insight = generate_insights(scores)
    keywords = ", ".join(get_top_keywords(text))

    return (
        f"🧠 **Overall Mentor Score:** {scores['Overall Mentor Score']} / 100\n\n"
        f"✨ Clarity: {scores['Clarity']}%\n"
        f"🎙️ Tone & Emotion: {scores['Tone']}%\n"
        f"📚 Knowledge Depth: {scores['Depth']}%\n"
        f"🔥 Engagement: {scores['Engagement']}%\n\n"
        f"🏅 **Rating:** {rating}\n"
        f"💬 **AI Insight:** {insight}\n"
        f"🗝️ **Top Keywords:** {keywords if keywords else 'N/A'}"
    )

demo = gr.Interface(
    fn=mentor_scoring_interface,
    inputs=[
        gr.Textbox(lines=8, label="Paste Mentor Transcript"),
        gr.Audio(source="upload", type="filepath", label="Upload Mentor Audio (optional)")
    ],
    outputs=gr.Markdown(label="Mentor Evaluation Report"),
    title="Mentor Scoring AI – Team NeuroLearn",
    description="AI system to evaluate mentors' clarity, tone, depth, and engagement.",
    article="Developed by Sameer Mishra – IIT Madras | Techfest IIT Bombay Round 2 Submission",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
