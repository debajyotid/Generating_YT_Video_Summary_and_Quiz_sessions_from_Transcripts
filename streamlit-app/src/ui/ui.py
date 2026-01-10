"""
UI Module for the Learn With AI Application.

This module defines the Streamlit user interface components used in the application.
It is structured into three main sections corresponding to the application's workflow:

1.  **Transcript Section**: Handles YouTube URL input, validation, and transcript fetching.
2.  **Primary Task Section**: Allows users to select and execute tasks like translation,
    summarization (Open Source or ChatGPT), step generation, or quiz generation.
3.  **Follow-up Section**: Provides options for further actions on the generated summary,
    such as translation, audio generation (TTS), and file downloading.

Dependencies:
    - streamlit: For rendering the web interface.
    - core.transcript: For YouTube video and transcript handling.
    - core.translation: For text translation functionalities.
    - core.summarization: For local summarization models.
    - core.gpt_utils: For OpenAI GPT-based interactions.
    - core.audio: For text-to-speech generation.
"""
import streamlit as st
from core.transcript import (extract_video_id, list_available_transcripts, get_transcript,)
from core.translation import (PREDEFINED_LANGS,get_translation_pipeline,translate_text,)
from core.summarization import (load_summarizer,summarize_text,)
from core.gpt_utils import (get_client,gpt_summary,gpt_steps,gpt_quiz,)
from core.audio import generate_audio

# ---------------------------------------------------------
# UI Section: Transcript Loader
# ---------------------------------------------------------
def ui_transcript_section():
    """
    Renders the Streamlit UI for the transcript loading section.

    This function handles the user interaction for:
    1. Entering a YouTube URL.
    2. Validating the URL and extracting the video ID.
    3. Fetching and displaying available transcript languages.
    4. Selecting a language and fetching the transcript text.

    Returns:
        tuple: A tuple containing (transcript_text, language_code, video_id).
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
            st.text_area("Transcript", text, height=200)
            return text, chosen_code, video_id

    except Exception as e:
        st.error(f"Error fetching transcripts: {e}")

    return None, None, None

# ---------------------------------------------------------
# UI Section: Primary Task Selector
# ---------------------------------------------------------
def ui_primary_task_section(transcript, transcript_lang, openai_key):
    """
    Renders the Streamlit UI for the primary task selection and execution.

    Allows the user to select a processing task to apply to the transcript.
    Supported tasks include:
    - Translation: Translates the transcript to a selected language.
    - Summarisation (Open Source): Summarizes using a local model.
    - Summarisation (ChatGPT): Summarizes using OpenAI's GPT model.
    - Steps (ChatGPT): Generates step-by-step instructions using GPT.
    - Quiz (ChatGPT): Generates a quiz based on the transcript using GPT.

    Args:
        transcript (str): The text of the video transcript.
        transcript_lang (str): The language code of the transcript.
        openai_key (str): The OpenAI API key provided by the user.

    Returns:
        tuple: A tuple containing (result_text, result_language_code).
               - For Translation and Summarisation tasks, returns the generated text and its language.
               - For Steps and Quiz tasks, or if no task is performed, returns (None, None).
    """
    st.header("Step 2: Primary Task")

    task = st.selectbox(
                            "Select a task",
                            [
                                "None",
                                "Translation",
                                "Summarisation (Open Source)",
                                "Summarisation (ChatGPT)",
                                "Steps (ChatGPT)",
                                "Quiz (ChatGPT)",
                            ],
                        )

    if task == "None" or transcript is None:
        return None, None

    # --- Translation ---
    if task == "Translation":
        tgt_label = st.selectbox("Translate to", list(PREDEFINED_LANGS.keys()))
        tgt_lang = PREDEFINED_LANGS[tgt_label]

        if st.button("Translate Transcript"):
            try:
                translator = get_translation_pipeline(transcript_lang, tgt_lang)
                with st.spinner("Translating..."):
                    translated = translate_text(transcript, translator)
                st.text_area(f"Translated to {tgt_label}", translated, height=200)
                st.download_button("Download Translation", translated, "translated.txt")
                return translated, tgt_lang
            except Exception as e:
                st.error(f"Translation error: {e}")

    # --- Summarisation (Open Source) ---
    if task == "Summarisation (Open Source)":
        if st.button("Summarise Transcript"):
            summarizer = load_summarizer()
            with st.spinner("Summarising..."):
                summary = summarize_text(transcript, summarizer)
            st.text_area("Summary (Open Source)", summary, height=200)
            return summary, transcript_lang

    # --- Summarisation (ChatGPT) ---
    if task == "Summarisation (ChatGPT)":
        if not openai_key:
            st.error("Enter OpenAI API key.")
            return None, None

        if st.button("Summarise with ChatGPT"):
            client = get_client(openai_key)
            with st.spinner("Summarising..."):
                summary = gpt_summary(client, transcript)
            st.text_area("Summary (ChatGPT)", summary, height=200)
            return summary, transcript_lang

    # --- Steps ---
    if task == "Steps (ChatGPT)":
        if not openai_key:
            st.error("Enter OpenAI API key.")
            return None, None

        if st.button("Generate Steps"):
            client = get_client(openai_key)
            with st.spinner("Generating steps..."):
                steps = gpt_steps(client, transcript)
            st.text_area("Steps", steps, height=250)
            st.download_button("Download Steps", steps, "steps.txt")
            return None, None

    # --- Quiz ---
    if task == "Quiz (ChatGPT)":
        if not openai_key:
            st.error("Enter OpenAI API key.")
            return None, None

        if st.button("Generate Quiz"):
            client = get_client(openai_key)
            with st.spinner("Generating quiz..."):
                quiz = gpt_quiz(client, transcript)
            st.text_area("Quiz", quiz, height=300)
            st.download_button("Download Quiz", quiz, "quiz.txt")
            return None, None

    return None, None

# ---------------------------------------------------------
# UI Section: Follow-up Actions on Summary
# ---------------------------------------------------------
def ui_followup_section(summary, summary_lang, openai_key):
    """
    Renders the Streamlit UI for follow-up actions on the generated summary.

    This section allows the user to perform additional operations on the summary text,
    such as translating it to another language, generating an audio version (TTS),
    or downloading the text file.

    Args:
        summary (str): The generated summary text.
        summary_lang (str): The language code of the summary text.
        openai_key (str): The OpenAI API key for audio generation.

    Returns:
        None
    """
    if summary is None:
        return

    st.header("Step 3: Follow-up Actions on Summary")
    st.text_area("Current Summary", summary, height=200)

    col1, col2, col3 = st.columns(3)

    # --- Translate Summary ---
    with col1:
        tgt_label = st.selectbox(
                                    "Translate summary to",
                                    list(PREDEFINED_LANGS.keys()),
                                    key="summary_translate",
                                )
        tgt_lang = PREDEFINED_LANGS[tgt_label]

        if st.button("Translate Summary"):
            try:
                translator = get_translation_pipeline(summary_lang, tgt_lang)
                with st.spinner("Translating summary..."):
                    translated = translate_text(summary, translator)
                st.text_area(f"Summary translated to {tgt_label}", translated, height=200)
                st.download_button("Download Translated Summary", translated, "summary_translated.txt")
            except Exception as e:
                st.error(f"Error translating summary: {e}")

    # --- Audio ---
    with col2:
        if not openai_key:
            st.info("Enter OpenAI key for audio.")
        else:
            if st.button("Generate Summary Audio"):
                client = get_client(openai_key)
                with st.spinner("Generating audio..."):
                    audio_bytes = generate_audio(summary, client)
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("Download Summary Audio", audio_bytes, "summary.mp3")

    # --- Download Summary ---
    with col3:
        st.download_button("Download Summary Text", summary, "summary.txt")