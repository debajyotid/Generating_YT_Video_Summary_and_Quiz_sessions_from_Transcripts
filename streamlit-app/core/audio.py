import io
import scipy.io.wavfile
import numpy as np
import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=False)
def load_audio_pipeline():
    """
    Loads and caches the TTS pipeline using the 'microsoft/VibeVoice-1.5B' model.

    Returns:
        transformers.Pipeline: The loaded text-to-speech pipeline.
    """
    return pipeline("text-to-speech", model="microsoft/VibeVoice-1.5B")

@st.cache_data(show_spinner=False)
def oss_audio(audio_gen_pipeline, text):
    """
    Generates audio from text using the provided pipeline, handling long text via chunking.

    Args:
        audio_gen_pipeline (transformers.Pipeline): The TTS pipeline.
        text (str): The text to convert to speech.

    Returns:
        bytes: The combined audio data in WAV format.

    Raises:
        ValueError: If audio generation fails for all chunks.
    """
    # Split text into chunks to provide progress updates
    words = text.split()
    chunk_size = 50  # Process ~50 words at a time
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    audio_parts = []
    sampling_rate = None
    progress_bar = st.progress(0)

    for i, chunk in enumerate(chunks):
        try:
            output = audio_gen_pipeline(chunk)
            if sampling_rate is None:
                sampling_rate = output["sampling_rate"]
            audio_parts.append(output["audio"])
        except Exception as e:
            st.warning(f"Skipping chunk {i+1} due to generation error: {e}")
        progress_bar.progress((i + 1) / len(chunks))

    if not audio_parts:
        raise ValueError("Audio generation failed for all text chunks.")

    final_audio = np.concatenate(audio_parts)
    buffer = io.BytesIO()
    scipy.io.wavfile.write(buffer, sampling_rate, final_audio)
    return buffer.getvalue()