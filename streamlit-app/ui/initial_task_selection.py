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
from core.gpt_utils import (ui_get_openai_client, gpt_summary,gpt_steps,gpt_quiz,)

# ---------------------------------------------------------
# UI Section: Primary Task Selector
# ---------------------------------------------------------
def _init_task_state():
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "summary_lang" not in st.session_state:
        st.session_state.summary_lang = None

def _handle_translation(transcript, transcript_lang):
    tgt_label = st.selectbox("Translate transcript to",list(PREDEFINED_LANGS.keys()),key="translate_transcript_tgt",)
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

def _handle_summarisation_os(transcript, transcript_lang):
    if st.button("Summarise Transcript", key="btn_summarise_os"):
        summarizer = load_summarizer()
        with st.spinner("Summarising transcript..."):
            summary = summarize_text(summarizer, transcript)
        st.text_area("Summary (Open Source)", summary, height=200)
        st.session_state.summary = summary
        st.session_state.summary_lang = transcript_lang

def _handle_summarisation_gpt(transcript, transcript_lang):
    client = ui_get_openai_client()
    if client:
        if st.button("Summarise with ChatGPT", key="btn_summarise_gpt"):
            with st.spinner("Summarising with ChatGPT..."):
                summary = gpt_summary(client, transcript)
            st.text_area("Summary (ChatGPT)", summary, height=200)
            st.session_state.summary = summary
            st.session_state.summary_lang = transcript_lang

def _handle_steps(transcript, transcript_lang):
    client = ui_get_openai_client()
    if client:
        if st.button("Generate Steps", key="btn_steps"):
            with st.spinner("Generating steps..."):
                steps = gpt_steps(client, transcript)
            st.text_area("Steps", steps, height=250)
            st.download_button("Download Steps", steps, "steps.txt")

def _handle_quiz(transcript, transcript_lang):
    client = ui_get_openai_client()
    if client:
        if st.button("Generate Quiz", key="btn_quiz"):
            with st.spinner("Generating quiz..."):
                quiz = gpt_quiz(client, transcript)
            st.text_area("Quiz", quiz, height=300)
            st.download_button("Download Quiz", quiz, "quiz.txt")

TASK_HANDLERS = {"Translation": _handle_translation,
                 "Summarisation (Open Source)": _handle_summarisation_os,
                 "Summarisation (ChatGPT)": _handle_summarisation_gpt,
                 "Steps (ChatGPT)": _handle_steps,
                 "Quiz (ChatGPT)": _handle_quiz,
                 }

def ui_primary_task_section():
    """
    Renders the Streamlit UI for the primary task selection and execution.

    Uses a configuration dictionary `TASK_HANDLERS` to dynamically render and execute
    the selected task.

    Supported Tasks:
    - Translation
    - Summarisation (Open Source & ChatGPT)
    - Steps Generation (ChatGPT)
    - Quiz Generation (ChatGPT)

    Updates `st.session_state` with results (e.g., summary) for downstream tasks.
    """
    st.header("Step 2: Primary Task")
    _init_task_state()

    transcript = st.session_state.get("transcript")
    transcript_lang = st.session_state.get("transcript_lang")

    task = st.selectbox(
                            "Select a task",
                            ["None"] + list(TASK_HANDLERS.keys()),
                            key="primary_task_select",
                        )

    if transcript is None:
        st.info("Load a transcript first in Step 1.")
        return

    if task in TASK_HANDLERS:
        TASK_HANDLERS[task](transcript, transcript_lang)