"""
UI Component: Transcript Form Renderer.

This module defines the user interface logic for the initial step of the application:
loading a YouTube video transcript. It handles URL input, validation, language selection, and transcript retrieval.

Dependencies:
    - streamlit: For rendering the UI components.
    - core.transcript: For backend logic related to YouTube video IDs and transcripts.
"""
import streamlit as st
from core.transcript import (extract_video_id, list_available_transcripts, get_transcript, generate_transcript_text)

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
    # Added for tracking manual upload of transcripts of automatic retrieval fails
    if "manual_mode" not in st.session_state:
        st.session_state.manual_mode = False
    # Added for tracking validation of OpenAI API key
    if "apikey_valid" not in st.session_state:
        st.session_state.apikey_valid = False
    if "openaiclient" not in st.session_state:
        st.session_state.openaiclient = None

def ui_render_refresh_button():
    """
    Renders a 'REFRESH' button to clear session state and reset the app.
    Displays a success message upon successful reset.
    """
    # Check if the app was just reset and display a success message
    if st.session_state.get("reset_success"):
        st.success("✅ App has been reset successfully.")
        del st.session_state["reset_success"]

    if st.button("REFRESH", type="primary", help="Clear all data and reset"):
        st.session_state.clear()
        st.session_state.reset_success = True
        st.rerun()

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
    st.subheader("Please provide a valid YouTube URL, or an audio/video file, for generating a transcript.")

    _init_transcript_state()

    youtube_url = st.text_input("Enter YouTube URL", value=st.session_state.get("youtube_url", ""))
    st.session_state.youtube_url = youtube_url  # persist URL

    uploaded_file = st.file_uploader("Upload a video (.mp4, .mkv, .mov, .avi) or audio file (.mp3, .wav, .flac, .m4a) for generating transcripts ",
                                    type=["mp4", "mkv", "mov", "avi", "mp3", "wav", "flac", "m4a"],
                                    key="video_audio_upload")

    # Load transcript options
    if st.button("Load Transcript Options", key="btn_load_transcripts"):
        # Check if a valid URL is provided
        if not youtube_url:
            # If no URL, check if file uploaded
            if uploaded_file:
                try:
                    text = generate_transcript_text(uploaded_file)
                    st.session_state.transcript = text
                    st.session_state.transcript_lang = "en" # Default to English for manual upload
                    st.session_state.manual_mode = False    # disable manual mode if file transcribed successfully
                    st.success("Transcript generated from uploaded file.")
                except Exception as e:
                    st.session_state.manual_mode = True # Enable manual mode if automatic retrieval fails
                    st.info("Unable to generate transcript from uploaded file. To proceed further, either upload/paste transcript in English below or retry with a different file.")
            else:          
                st.error("Please enter a YouTube URL or upload a video/audio file.")
        # Proceeding to process provided URL
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
                        st.session_state.manual_mode = False  # disable manual mode if options loaded successfully
                        st.success("Transcript options loaded.")
                except Exception as e:
                    st.session_state.manual_mode = True # Enable manual mode if automatic retrieval fails
                    st.info("Automatic transcript retrieval failed. Please upload or paste the transcript in English, manually below.")
                    
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
                        st.session_state.manual_mode = False  # disable manual mode if transcript fetched automatically
                        st.success("Transcript fetched successfully.")
                    except Exception as e:
                        st.session_state.manual_mode = True # Enable manual mode if automatic retrieval fails
                        st.info("Automatic transcript retrieval failed. Please upload or paste the transcript in English, manually below.")

    # Adding the below info to guide user for manual transcript input as fallback
    # ---------------------------------------------------------
    # Manual transcript fallback (upload or paste)
    # ---------------------------------------------------------    
    if st.session_state.manual_mode and st.session_state.transcript is None:        
        st.markdown("### 📄 Upload Transcript Manually")
        uploaded_text_file = st.file_uploader("Upload transcript file (.txt, .srt, .vtt)",
                                              type=["txt", "srt", "vtt"],
                                              key="manual_transcript_upload")
        
        if uploaded_text_file:
            try:
                text = uploaded_text_file.read().decode("utf-8")
                st.session_state.transcript = text
                st.session_state.transcript_lang = "en" # Default to English for manual upload
                st.success("Transcript loaded from uploaded file.")
            except Exception as e:
                st.error(f"Could not read uploaded file: {e}")

        manual_text = st.text_area("Or paste transcript manually", key="manual_transcript_paste")

        if manual_text.strip():
            st.session_state.transcript = manual_text.strip()
            st.session_state.transcript_lang = "en" # Default to English for manual upload
            st.success("Transcript loaded from manual input.")

    # Always show transcript if present
    if st.session_state.transcript:
        st.text_area("Transcript", st.session_state.transcript, height=200)