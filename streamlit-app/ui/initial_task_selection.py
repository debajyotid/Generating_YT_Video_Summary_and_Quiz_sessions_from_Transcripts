"""
UI Component: Primary Task Selection.

This module defines the user interface logic for the second step of the application:
selecting and executing a primary task on the loaded transcript. Supported tasks include
translation, summarization (local or GPT-based), step generation, and quiz creation.

Dependencies:
    - streamlit: For rendering the UI components.
    - core.translation: For translation logic.
    - core.summarization: For open-source summarization.
    - core.gpt_utils: For GPT-based tasks (summary, steps, quiz).
"""
import streamlit as st

from core.translate import (PREDEFINED_LANGS,get_translation_pipeline,translate_text,)
from core.summarization import (load_summarizer,summarize_text,)
from core.gpt_utils import (get_client,gpt_summary,gpt_steps,gpt_quiz,)

# ---------------------------------------------------------
# UI Section: Primary Task Selector
# ---------------------------------------------------------
def _init_task_state():
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "summary_lang" not in st.session_state:
        st.session_state.summary_lang = None

def ui_primary_task_section():
    """
    Renders the Streamlit UI for the primary task selection and execution.

    This function presents a selection box to the user to choose a processing task
    for the video transcript. Based on the selection, it invokes the corresponding
    backend logic and displays the results.

    Supported Tasks:
    1.  **Translation**: Translates the transcript to a target language.
    2.  **Summarisation (Open Source)**: Generates a summary using a local Hugging Face model.
    3.  **Summarisation (ChatGPT)**: Generates a summary using OpenAI's GPT models.
    4.  **Steps (ChatGPT)**: Extracts step-by-step instructions using OpenAI's GPT models.
    5.  **Quiz (ChatGPT)**: Generates a multiple-choice quiz using OpenAI's GPT models.

    Returns:
        tuple[str | None, str | None]: A tuple containing (result_text, result_language_code).
        (None, None) if no task is selected or if the task (like Steps/Quiz) does not produce a chainable text result.
    """
    st.header("Step 2: Primary Task")
    _init_task_state()

    transcript = st.session_state.get("transcript")
    transcript_lang = st.session_state.get("transcript_lang")

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
                            key="primary_task_select",
                        )

    if transcript is None:
        st.info("Load a transcript first in Step 1.")
        return

    # --- Translation ---
    if task == "Translation":
        tgt_label = st.selectbox("Translate transcript to",
                                 list(PREDEFINED_LANGS.keys()),
                                 key="translate_transcript_tgt",
                                 )
        tgt_lang = PREDEFINED_LANGS[tgt_label]

        if st.button("Translate Transcript", key="btn_translate_transcript"):
            try:
                translator = get_translation_pipeline(transcript_lang, tgt_lang)
                with st.spinner("Translating transcript..."):
                    translated = translate_text(transcript, translator)
                st.text_area(f"Transcript translated to {tgt_label}",translated,height=200,)
                st.download_button("Download Translation", translated, "translated.txt")
            except Exception as e:
                st.error(f"Translation error: {e}")

    # --- Summarisation (Open Source) ---
    if task == "Summarisation (Open Source)":
        if st.button("Summarise Transcript", key="btn_summarise_os"):
            summarizer = load_summarizer()
            with st.spinner("Summarising transcript..."):
                summary = summarize_text(transcript, summarizer)
            st.text_area("Summary (Open Source)", summary, height=200)
            st.session_state.summary = summary
            st.session_state.summary_lang = transcript_lang

    # --- Summarisation (ChatGPT) ---
    if task == "Summarisation (ChatGPT)":
        if "openai_key" not in st.session_state:
            st.session_state.openai_key = ""
        # Render the input box
        st.session_state.openai_key = st.text_input("Enter your OpenAI API Key to use ChatGPT tasks.", type="password", value=st.session_state.openai_key)
        # Only show the button if a key is entered
        if st.session_state.openai_key.strip() != "":
            client, err = get_client(st.session_state.openai_key)
            if err:
                st.error("❌ Invalid API key. Please try again.")
                st.session_state.openai_key = ""                            # Reset the key so the input box becomes empty + highlighted    
                st.experimental_rerun()                                     # Force rerun so the input box reappears immediately
                st.stop()
            else:
                st.success("✅ API key validated successfully.")
                if st.button("Summarise with ChatGPT", key="btn_summarise_gpt"):
                    client, err = get_client(st.session_state.openai_key)
                    if err:
                        st.error(err)
                        st.session_state.openai_key = ""                            # Reset the key so the input box becomes empty + highlighted
                        st.experimental_rerun()                                     # Force rerun so the input box reappears immediately
                        st.stop()
                    else:
                        with st.spinner("Summarising with ChatGPT..."):
                            summary = gpt_summary(client, transcript)
                        st.text_area("Summary (ChatGPT)", summary, height=200)
                        st.session_state.summary = summary
                        st.session_state.summary_lang = transcript_lang

    # --- Steps (ChatGPT) ---
    if task == "Steps (ChatGPT)":
        if "openai_key" not in st.session_state:
            st.session_state.openai_key = ""
        # Render the input box
        st.session_state.openai_key = st.text_input("Enter your OpenAI API Key to use ChatGPT tasks.", type="password", value=st.session_state.openai_key)        
        # Only show the button if a key is entered
        if st.session_state.openai_key.strip() != "":
            client, err = get_client(st.session_state.openai_key)
            if err:
                st.error("❌ Invalid API key. Please try again.")
                st.session_state.openai_key = ""                            # Reset the key so the input box becomes empty + highlighted    
                st.experimental_rerun()                                     # Force rerun so the input box reappears immediately
                st.stop()
            else:
                st.success("✅ API key validated successfully.")
                if st.button("Generate Steps", key="btn_steps"):
                    with st.spinner("Generating steps..."):
                        steps = gpt_steps(client, transcript)
                    st.text_area("Steps", steps, height=250)
                    st.download_button("Download Steps", steps, "steps.txt")

    # --- Quiz (ChatGPT) ---
    if task == "Quiz (ChatGPT)":
        if "openai_key" not in st.session_state:
            st.session_state.openai_key = ""
        # Render the input box
        st.session_state.openai_key = st.text_input("Enter your OpenAI API Key to use ChatGPT tasks.", type="password", value=st.session_state.openai_key)        
        # Only show the button if a key is entered
        if st.session_state.openai_key.strip() != "":
            client, err = get_client(st.session_state.openai_key)
            if err:
                st.error("❌ Invalid API key. Please try again.")
                st.session_state.openai_key = ""                            # Reset the key so the input box becomes empty + highlighted    
                st.experimental_rerun()                                     # Force rerun so the input box reappears immediately
                st.stop()
            else:
                st.success("✅ API key validated successfully.")            
                if st.button("Generate Quiz", key="btn_quiz"):
                    with st.spinner("Generating quiz..."):
                        quiz = gpt_quiz(client, transcript)
                    st.text_area("Quiz", quiz, height=300)
                    st.download_button("Download Quiz", quiz, "quiz.txt")