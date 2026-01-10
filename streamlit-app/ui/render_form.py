"""
UI Component: Transcript Form Renderer.

This module defines the user interface logic for the initial step of the application:
loading a YouTube video transcript. It handles URL input, validation, language selection, and transcript retrieval.

Dependencies:
    - streamlit: For rendering the UI components.
    - core.transcript: For backend logic related to YouTube video IDs and transcripts.
"""
import streamlit as st
from core.transcript import (extract_video_id, list_available_transcripts, get_transcript,)

# ---------------------------------------------------------
# UI Section: Transcript Loader
# ---------------------------------------------------------
def ui_initial_form_renderer():
    """
    Renders the Streamlit UI for the transcript loading section.

    This function manages the following user interactions:
    1.  **Input**: Accepts a YouTube URL from the user.
    2.  **Validation**: Validates the URL and extracts the video ID.
    3.  **Selection**: Fetches available transcript languages and allows the user to select one.
    4.  **Retrieval**: Fetches the transcript text for the selected language.

    Returns:
        tuple[str | None, str | None, str | None]: A tuple containing:
            - transcript_text (str): The full text of the transcript.
            - language_code (str): The selected language code (e.g., 'en').
            - video_id (str): The extracted YouTube video ID.
            Returns (None, None, None) if the transcript is not loaded or an error occurs.
    """
    st.header("Step 1: Transcript")

    youtube_url = st.text_input("Enter YouTube URL")
    load_btn = st.button("Load Transcript Options")

    if not load_btn:
        return None, None, None

    if not youtube_url:
        st.error("Please enter a YouTube URL.")
        return None, None, None

    video_id = extract_video_id(youtube_url)
    if not video_id:
        st.error("Invalid YouTube URL.")
        return None, None, None

    try:
        available = list_available_transcripts(video_id)
        if not available:
            st.error("No transcripts available for this video.")
            return None, None, None

        st.success("Transcript options loaded.")
        lang_display = [f"{code} - {name}" for code, name in available]
        choice = st.selectbox("Choose transcript language", lang_display)
        chosen_code = choice.split(" - ")[0]

        if st.button("Fetch Transcript"):
            text = get_transcript(video_id, chosen_code)
            st.markdown("#### Transcript:")
            st.write(text)
            st.download_button("Download Transcript", text, "transcript.txt")
            return text, chosen_code, video_id

    except Exception as e:
        st.error(f"Error fetching transcripts: {e}")

    return None, None, None