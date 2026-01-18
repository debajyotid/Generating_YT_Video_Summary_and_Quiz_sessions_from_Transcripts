"""
Transcript Module.

This module handles interactions with YouTube to extract video information and retrieve transcripts.
It uses the `youtube_transcript_api` to fetch transcripts in various languages.

Dependencies:
    - youtube_transcript_api: For fetching transcripts.
    - streamlit: For caching results.
"""
import re
import textwrap
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

# Map human labels to YouTube language codes
LANG_LABELS = {"English": "en",
               "Spanish": "es",
               "French": "fr",
               "German": "de",
               "Portuguese": "pt",}

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
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
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
    ytt = YouTubeTranscriptApi()
    if language_code:
        #transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        transcript = ytt.fetch(video_id, languages=[language_code]) #--- EDITED --- modified to use instance method as per recent changes
    else:
        #transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ytt.fetch(video_id) #--- EDITED --- modified to use instance method as per recent changes
    return " ".join([seg["text"] for seg in transcript])
