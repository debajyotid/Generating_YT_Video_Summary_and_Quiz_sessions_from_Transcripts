"""
Transcript Module.

This module handles interactions with YouTube to extract video information and retrieve transcripts.
It uses the 'youtube_transcript_api' library to fetch transcripts in various languages.

Dependencies:
    - youtube_transcript_api: For fetching transcripts.
    - streamlit: For caching results.
"""
import re
import torch
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Map human labels to YouTube language codes
# LANG_LABELS = {"English": "en",
#                "Spanish": "es",
#                "French": "fr",
#                "German": "de"}

def extract_video_id(url: str):
    """
    Extracts the YouTube video ID from a standard YouTube URL.

    Args:
        url (str): The full YouTube video URL (e.g., "https://www.youtube.com/watch?v=...").

    Returns:
        str | None: The extracted video ID if found, otherwise None.
    """
    match = re.search(r"v=([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None

@st.cache_data(show_spinner=False)
def list_available_transcripts(video_id):
    """
    Retrieves a list of available transcript languages for a given video ID.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        list[tuple[str, str]]: A list of tuples containing (language_code, language_name).
    """
    transcript_list = YouTubeTranscriptApi().list(video_id)
    options = []
    for tr in transcript_list:
        lang_code = tr.language_code
        lang_name = tr.language
        options.append((lang_code, lang_name))
    return options

@st.cache_data(show_spinner=False)
def get_transcript(video_id, language_code=None):
    """
    Fetches the full transcript text for a specific video and language.

    Args:
        video_id (str): The YouTube video ID.
        language_code (str, optional): The language code (e.g., 'en', 'es').
                                       If None, fetches the default transcript.

    Returns:
        str: The concatenated text of the transcript.
    """
    if language_code:
        #transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript =  YouTubeTranscriptApi().fetch(video_id, languages=[language_code]) #--- EDITED --- modified to use instance method as per recent changes
    else:
        #transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi().fetch(video_id) #--- EDITED --- modified to use instance method as per recent changes
    return " ".join([seg["text"] for seg in transcript])

@st.cache_resource(show_spinner=False)
def load_external_file():
    """
    Loads and caches the automatic speech recognition pipeline using the 'openai/whisper-large-v3' model.

    Returns:
        transformers.Pipeline: The loaded ASR pipeline configured for chunked execution.
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, 
                                                      torch_dtype=torch_dtype, 
                                                      low_cpu_mem_usage=True, 
                                                      use_safetensors=True)
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline("automatic-speech-recognition",
                    model=model_id,
                    chunk_length_s=30,                              # Enabling the chunked algorithm instead of the default sequential, with optimal chunk length of 30s for 'large-v3'
                    tokenizer=processor.tokenizer,
                    feature_extractor=processor.feature_extractor,
                    torch_dtype=torch_dtype,
                    device=device,)
    return pipe

@st.cache_data(show_spinner=False)
def generate_transcript_text(uplded_vid_aud_file):
    """
    Generates a transcript from an uploaded video or audio file using a local Whisper model.

    Args:
        uplded_vid_aud_file (UploadedFile): The file uploaded via Streamlit.

    Returns:
        str: The transcribed text in English.
    """
    pipe = load_external_file()
    result = pipe(uplded_vid_aud_file, generate_kwargs={"task": "translate"})  # Generating the transcribed text in English 
    return (result["text"])
