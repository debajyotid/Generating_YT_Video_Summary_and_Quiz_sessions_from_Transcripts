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
from core.audio import load_audio_piepeline, oss_audio
from core.gpt_utils import ui_get_openai_client, gpt_audio

# ---------------------------------------------------------
# UI Section: Follow-up Actions on Summary
# ---------------------------------------------------------
def ui_followup_section():
    """
    Renders the Streamlit UI for follow-up actions on the generated summary.

    This function provides a set of tools to further utilize the generated summary:
    1.  **Translation**: Translates the summary into a selected target language.
    2.  **Audio Generation**: Converts the summary text into speech using OpenAI's TTS API.
    3.  **Download**: Allows the user to download the summary as a text file.

    Returns:
        None
    """
    summary = st.session_state.get("summary")
    summary_lang = st.session_state.get("summary_lang")

    if not summary:
        st.info("Run a summarisation task in Step 2 to enable follow-up actions.")
        return

    st.header("Step 3: Follow-up Actions on Summary")
    st.text_area("Current Summary", summary, height=200)

    task = st.selectbox(
                        "Select a task",
                        [
                            "Download Summary",
                            "Summary Translation",
                            "Summary Audio (Open Source)",
                            "Summary Audio (ChatGPT)",
                        ],
                        key="followup_task_select",
                    )
    # --- Download Summary ---
    if task == "Download Summary":
        st.download_button("Download Summary Text", summary, "summary.txt")

    # --- Translate Summary ---
    if task == "Summary Translation":
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

    # --- Audio (Open Source) ---
    if task == "Summary Audio (Open Source)":
        if st.button("Generate Summary Audio", key="btn_summary_audio"):
            audio_gen = load_audio_piepeline()
            with st.spinner("Generating audio..."):
                audio_bytes = oss_audio(summary, audio_gen)
            st.audio(audio_bytes, format="audio/wav")
            st.download_button("Download Summary Audio", audio_bytes, "summary.wav")

    # --- Audio (GPT) ---
    if task == "Summary Audio (ChatGPT)":
        client = ui_get_openai_client()
        if client:
            if st.button("Generate Summary Audio", key="btn_summary_audio"):
                with st.spinner("Generating audio..."):
                    audio_bytes = gpt_audio(summary, client)
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("Download Summary Audio", audio_bytes, "summary.mp3")