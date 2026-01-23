import streamlit as st

@st.cache_data(show_spinner=False)
def generate_audio(text, _client):
    """
    Generates speech audio from text using OpenAI's Text-to-Speech API.

    This function uses the specified OpenAI client to convert the input text
    into audio using the 'gpt-4o-mini-tts' model and 'alloy' voice.
    The result is cached by Streamlit to avoid redundant API calls.

    Args:
        text (str): The text content to convert to speech.
        client (openai.OpenAI): An initialized OpenAI client instance.

    Returns:
        bytes: The binary content of the generated audio file.
    """
    speech = _client.audio.speech.create(
                                            model="gpt-4o-mini-tts",
                                            voice="alloy",
                                            input=text
                                        )
    return speech.read()