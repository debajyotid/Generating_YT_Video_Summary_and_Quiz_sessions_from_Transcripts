"""
UI Component: Follow-up Task Actions.

This module defines the user interface logic for the final step of the application:
performing follow-up actions on the generated summary. This includes translating the
summary, converting it to speech (audio), and downloading the results.

Dependencies:
    - streamlit: For rendering the UI components.
    - core.translation: For translating the summary text.
    - core.gpt_utils: For initializing the OpenAI client (used in TTS).
    - core.audio: For generating audio from text.
"""
import streamlit as st

from core.translate import (PREDEFINED_LANGS,get_translation_pipeline,translate_text,)
from core.audio import load_audio_pipeline, oss_audio
from core.gpt_utils import ui_get_openai_client, gpt_audio

# ---------------------------------------------------------
# UI Section: Follow-up Actions on Summary
# ---------------------------------------------------------
def _handle_download(summary, summary_lang):
    st.download_button("Download Summary Text", summary, "summary.txt")

def _handle_translation(summary, summary_lang):
    tgt_label = st.selectbox("Translate summary to", list(PREDEFINED_LANGS.keys()), key="summary_translate_tgt",)
    tgt_lang = PREDEFINED_LANGS[tgt_label]

    if st.button("Translate Summary", key="btn_translate_summary"):
        try:
            translator = get_translation_pipeline(summary_lang, tgt_lang)
            with st.spinner("Translating summary..."): translated = translate_text(summary, translator)
            st.text_area(f"Summary translated to {tgt_label}",translated,height=200,)
            st.download_button("Download Translated Summary",translated,"summary_translated.txt",)
        except Exception as e:
            st.error(f"Error translating summary: {e}")

def _handle_audio_os(summary, summary_lang):
    if st.button("Generate Summary Audio", key="btn_summary_audio"):
        audio_gen = load_audio_pipeline()
        with st.spinner("Generating audio..."):
            audio_bytes = oss_audio(audio_gen, summary)
        st.audio(audio_bytes, format="audio/wav")
        st.download_button("Download Summary Audio", audio_bytes, "summary.wav")

def _handle_audio_gpt(summary, summary_lang):
    client = ui_get_openai_client()
    if client:
        if st.button("Generate Summary Audio", key="btn_summary_audio"):
            with st.spinner("Generating audio..."):
                audio_bytes = gpt_audio(summary, client)
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Download Summary Audio", audio_bytes, "summary.mp3")

FOLLOWUP_HANDLERS = {"Download Summary": _handle_download,
                     "Summary Translation": _handle_translation,
                     "Summary Audio (Open Source)": _handle_audio_os,
                     "Summary Audio (ChatGPT)": _handle_audio_gpt,
                     }

def ui_followup_section():
    """
    Renders the Streamlit UI for follow-up actions on the generated summary.

    Uses a configuration dictionary `FOLLOWUP_HANDLERS` to dynamically render and execute
    the selected action.

    Supported Actions:
    - Download Summary
    - Translate Summary
    - Generate Audio (Open Source & ChatGPT)
    """
    summary = st.session_state.get("summary")
    summary_lang = st.session_state.get("summary_lang")

    if not summary:
        st.info("Run a summarisation task in Step 2 to enable follow-up actions.")
        return

    st.header("Step 3: Follow-up Actions on Summary")
    st.text_area("Current Summary", summary, height=200)

    task = st.selectbox("Select a task",
                        list(FOLLOWUP_HANDLERS.keys()),
                        key="followup_task_select",
                        )
    
    if task in FOLLOWUP_HANDLERS:
        FOLLOWUP_HANDLERS[task](summary, summary_lang)