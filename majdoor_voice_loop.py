import streamlit as st
import numpy as np
from scipy.io.wavfile import write as write_wav
import tempfile
import requests
from faster_whisper import WhisperModel

# Load model
@st.cache_resource
def load_model():
    return WhisperModel("base", compute_type="int8")

model, _ = load_model()

def get_openai_voice(text, voice="alloy", lang="English"):
    url = "https://nihalgazi-text-to-speech-unlimited.hf.space/api/predict"
    data = {"data": [text, voice, lang]}
    try:
        response = requests.post(url, json=data, timeout=60)
        return response.json()["data"][0]
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

def transcribe_audio(audio_path):
    segments, _ = model.transcribe(audio_path)
    return " ".join([segment.text for segment in segments])

def get_sarcastic_reply(user_text):
    from g4f.client import Client
    client = Client()
    prompt = f"""You are Majdoor AI, a sarcastic, desi, emotional assistant.
User said: '{user_text}'
Reply in Hinglish with desi sarcasm, mocking tone, and funny insult. Keep it short (1–2 lines)."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Bhai, GPT ka dimaag garam hai abhi..."

# UI
st.set_page_config(page_title="Majdoor AI - Voice Upload", page_icon="🧠")
st.title("🧠 Majdoor AI – Voice Upload to Response")
st.markdown("📤 Upload voice → 🧠 GPT reply → 🎧 AI speaks it")

voice = st.selectbox("🎙️ Voice", ["alloy", "nova", "shimmer"], index=0)
lang = st.selectbox("🌐 Language", ["English", "Hindi"], index=0)

uploaded_file = st.file_uploader("📂 Upload a WAV file", type=["wav"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(uploaded_file.read())
        temp_path = f.name
        user_text = transcribe_audio(temp_path)
        st.markdown(f"🧍 You said: **{user_text}**")

        response_text = get_sarcastic_reply(user_text)
        st.markdown(f"🤖 Majdoor: **{response_text}**")

        audio_url = get_openai_voice(response_text, voice, lang)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
