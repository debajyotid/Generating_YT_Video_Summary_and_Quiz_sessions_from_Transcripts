import io
import scipy.io.wavfile
import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=False)
def load_audio_piepeline():
    """
    Loads and caches the TTS pipeline using the 'microsoft/VibeVoice-1.5B' model.

    Returns:
        transformers.Pipeline: The loaded summarization pipeline.
    """
    return pipeline("text-to-speech", model="microsoft/VibeVoice-1.5B")

@st.cache_data(show_spinner=False)
def oss_audio(audio_gen_pipeline, text):
    """
    Generates audio from text using the provided pipeline.

    Args:
        text (str): The text to convert to speech.
        _audio_gen_pipeline (transformers.Pipeline): The TTS pipeline.

    Returns:
        bytes: The audio data in WAV format.
    """
    output = audio_gen_pipeline(text)
    buffer = io.BytesIO()
    scipy.io.wavfile.write(buffer, output["sampling_rate"], output["audio"])
    return buffer.getvalue()