
import streamlit as st
import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wav
import tempfile
import requests

# Load Whisper model only once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# TTS using Alloy/Nova/Shimmer without API key (via Hugging Face app)
def get_openai_voice(text, voice="alloy", lang="English"):
    url = "https://nihalgazi-text-to-speech-unlimited.hf.space/api/predict"
    data = {"data": [text, voice, lang]}
    try:
        response = requests.post(url, json=data, timeout=60)
        return response.json()["data"][0]
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

# Record mic input
def record_audio(duration=5, samplerate=16000):
    st.info("🎙️ Speak now...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return samplerate, recording

# Save to temp .wav
def save_temp_wav(samplerate, recording):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav.write(f.name, samplerate, recording)
        return f.name

# Transcribe audio
def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

# GPT4Free sarcastic reply
def get_sarcastic_reply(user_text):
    from g4f.client import Client
    client = Client()
    prompt = f"""
    You are Majdoor AI, an emotional, sarcastic Indian assistant.
    The user said: "{user_text}"

    Respond with Hinglish. Add sarcasm, emotional tone, maybe a funny insult.
    Keep it short, funny, and real. 1–2 lines max.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Bhai, GPT ka dimaag garam hai abhi..."

# Streamlit UI
st.set_page_config(page_title="Majdoor AI - Voice to Voice", page_icon="🧠")
st.title("🧠 Majdoor AI – Voice to Voice Chat")
st.markdown("🔁 Speak → Transcribe → GPT Reply → Speak Back")

voice = st.selectbox("🗣️ Voice", ["alloy", "nova", "shimmer"], index=0)
lang = st.selectbox("🌐 Language", ["English", "Hindi"], index=0)
duration = st.slider("⏱️ Record Duration (sec)", 2, 10, 5)

if st.button("🎬 Start Chat"):
    sr, audio = record_audio(duration=duration)
    audio_path = save_temp_wav(sr, audio)
    user_text = transcribe_audio(audio_path)
    st.markdown(f"🧍‍♂️ You said: **{user_text}**")
    
    response_text = get_sarcastic_reply(user_text)
    st.markdown(f"🤖 Majdoor: **{response_text}**")
    
    tts_url = get_openai_voice(response_text, voice, lang)
    if tts_url:
        st.audio(tts_url, format="audio/mp3")
