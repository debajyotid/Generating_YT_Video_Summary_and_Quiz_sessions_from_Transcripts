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

    # Initialize session state
    if "transcript_options_loaded" not in st.session_state:
        st.session_state.transcript_options_loaded = False
    if "available_transcripts" not in st.session_state:
        st.session_state.available_transcripts = None
    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "transcript_lang" not in st.session_state:
        st.session_state.transcript_lang = None
    if "video_id" not in st.session_state:
        st.session_state.video_id = None

    # --- YouTube URL Input ---
    try:
        youtube_url = st.text_input("Enter YouTube URL")
        if not youtube_url:
            st.warning("Please enter a YouTube URL.")
            return None, None, None
    except Exception as e:
        st.error(f"Error processing URL input: {e}")
        return None, None, None
        
    # --- Load transcript options ---
    if st.button("Load Transcript Options"):
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
            return None, None, None
        else:
            try:
                options = list_available_transcripts(video_id)
                if not options:
                    st.error("No transcripts available for this video.")
                    return None, None, None
                else:                   
                    st.session_state.available_transcripts = options
                    st.session_state.video_id = video_id
                    st.session_state.transcript_options_loaded = True
                    st.success("Transcript options loaded.")
            except Exception as e:
                st.error(f"Error fetching transcripts: {e}")

    # --- Show transcript language selector ---
    if st.session_state.transcript_options_loaded:
        lang_display = [ f"{code} - {name}" for code, name in st.session_state.available_transcripts]
        choice = st.selectbox("Choose transcript language", lang_display)
        chosen_code = choice.split(" - ")[0]

        # Fetch transcript button
        if st.button("Fetch Transcript"):
            try:
                text = get_transcript(st.session_state.video_id, chosen_code)
                st.session_state.transcript = text
                st.session_state.transcript_lang = chosen_code
                st.success("Transcript fetched successfully.")
            except Exception as e:
                st.error(f"Error retrieving transcript: {e}")

    # --- Always show transcript if available ---
    if st.session_state.transcript:
        st.text_area("Transcript", st.session_state.transcript, height=200)

    return (st.session_state.transcript,
            st.session_state.transcript_lang,
            st.session_state.video_id,)