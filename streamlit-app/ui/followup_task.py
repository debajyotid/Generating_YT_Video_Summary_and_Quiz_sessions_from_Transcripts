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

    col1, col2, col3 = st.columns([1,1,1])

    # --- Translate Summary ---
    with col1:
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

    # --- Audio ---
    with col2:
        if (("openai_key" not in st.session_state) or (st.session_state.openai_key.strip() == "")):
            st.session_state.openai_key = ""
            # Render the input box
            st.session_state.openai_key = st.text_input("Enter your OpenAI API Key to use ChatGPT tasks.", type="password", value=st.session_state.openai_key)
        # Only show the button if a key is entered
        if st.session_state.openai_key.strip() != "":
            # if the API Key hasdn't been validated yet
            if not st.session_state.apikey_valid:
                client, err = get_client(st.session_state.openai_key)                    
                if err:
                    st.error(f"❌ {err}")
                    st.session_state.openai_key = ""                            # Reset the key so the input box becomes empty + highlighted
                    st.session_state.apikey_valid = False    
                    st.rerun(scope="fragment")                                        # Queue for rerun so the input box reappears immediately
                else:
                    st.success("✅ API key validated successfully.")
                    st.session_state.apikey_valid = True                        # Mark the key as valid
                    if st.button("Generate Summary Audio", key="btn_summary_audio"):
                        with st.spinner("Generating audio..."):
                            audio_bytes = generate_audio(summary, client)
                        st.audio(audio_bytes, format="audio/mp3")
                        st.download_button("Download Summary Audio", audio_bytes, "summary.mp3")
            else:
                if st.button("Generate Summary Audio", key="btn_summary_audio"):
                    with st.spinner("Generating audio..."):
                        audio_bytes = generate_audio(summary, client)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("Download Summary Audio", audio_bytes, "summary.mp3")                

    # --- Download Summary ---
    with col3:
        st.download_button("Download Summary Text", summary, "summary.txt")