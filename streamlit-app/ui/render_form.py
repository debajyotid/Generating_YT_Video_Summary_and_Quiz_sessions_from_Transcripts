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
def _init_transcript_state():
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

    _init_transcript_state()

    youtube_url = st.text_input("Enter YouTube URL", value=st.session_state.get("youtube_url", ""))
    st.session_state.youtube_url = youtube_url  # persist URL

    # Load transcript options
    if st.button("Load Transcript Options", key="btn_load_transcripts"):
        if not youtube_url:
            st.error("Please enter a YouTube URL.")
        else:
            video_id = extract_video_id(youtube_url)
            if not video_id:
                st.error("Invalid YouTube URL.")
            else:
                try:
                    options = list_available_transcripts(video_id)
                    if not options:
                        st.error("No transcripts available for this video.")
                    else:
                        st.session_state.available_transcripts = options
                        st.session_state.video_id = video_id
                        st.session_state.transcript_options_loaded = True
                        st.success("Transcript options loaded.")
                except Exception as e:
                    st.error(f"Error fetching transcripts: {e}")
                    # Adding the below info to guide user for manual transcript input as fallback
                    st.info("Automatic transcript retrieval failed. Please upload or paste the transcript manually below.")

    # Language selection (if options loaded)
    if st.session_state.transcript_options_loaded and st.session_state.available_transcripts:
        lang_display = [f"{code} - {name}" for code, name in st.session_state.available_transcripts]
        # keep previous selection if possible
        default_index = 0
        if st.session_state.transcript_lang:
            for i, (code, _) in enumerate(st.session_state.available_transcripts):
                if code == st.session_state.transcript_lang:
                    default_index = i
                    break

        choice = st.selectbox("Choose transcript language",
                              lang_display,
                              index=default_index,
                              key="transcript_lang_select",)
        chosen_code = choice.split(" - ")[0]

        if st.button("Fetch Transcript", key="btn_fetch_transcript"):
            try:
                text = get_transcript(st.session_state.video_id, chosen_code)
                st.session_state.transcript = text
                st.session_state.transcript_lang = chosen_code
                st.success("Transcript fetched successfully.")
            except Exception as e:
                st.error(f"Error retrieving transcript: {e}")

    # ---------------------------------------------------------
    # Manual transcript fallback (upload or paste)
    # ---------------------------------------------------------
    st.subheader("If automatic transcript retrieval fails, add transcript manually")

    uploaded_file = st.file_uploader("Upload transcript file (.txt, .srt, .vtt)",
                                     type=["txt", "srt", "vtt"],
                                     key="manual_transcript_upload")

    if uploaded_file:
        try:
            text = uploaded_file.read().decode("utf-8")
            st.session_state.transcript = text
            st.session_state.transcript_lang = "manual"
            st.success("Transcript loaded from uploaded file.")
        except Exception as e:
            st.error(f"Could not read uploaded file: {e}")

    manual_text = st.text_area("Or paste transcript manually", key="manual_transcript_paste")

    if manual_text.strip():
        st.session_state.transcript = manual_text.strip()
        st.session_state.transcript_lang = "manual"
        st.success("Transcript loaded from manual input.")

    # Always show transcript if present
    if st.session_state.transcript:
        st.text_area("Transcript", st.session_state.transcript, height=200)