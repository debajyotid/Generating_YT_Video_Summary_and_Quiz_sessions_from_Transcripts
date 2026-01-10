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
from core.gpt_utils import (get_client,)
from core.audio import generate_audio

# ---------------------------------------------------------
# UI Section: Follow-up Actions on Summary
# ---------------------------------------------------------
def ui_followup_section(summary, summary_lang, openai_key):
    """
    Renders the Streamlit UI for follow-up actions on the generated summary.

    This function provides a set of tools to further utilize the generated summary:
    1.  **Translation**: Translates the summary into a selected target language.
    2.  **Audio Generation**: Converts the summary text into speech using OpenAI's TTS API.
    3.  **Download**: Allows the user to download the summary as a text file.

    Args:
        summary (str | None): The generated summary text. If None, the section is skipped.
        summary_lang (str): The language code of the summary text (e.g., 'en').
        openai_key (str): The OpenAI API key (required for audio generation).

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