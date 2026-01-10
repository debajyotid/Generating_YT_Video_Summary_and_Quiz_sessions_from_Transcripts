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
def ui_primary_task_section(transcript, transcript_lang, openai_key):
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

    Args:
        transcript (str): The full text of the video transcript.
        transcript_lang (str): The language code of the original transcript (e.g., 'en').
        openai_key (str): The OpenAI API key provided by the user (required for GPT tasks).

    Returns:
        tuple[str | None, str | None]: A tuple containing (result_text, result_language_code).
            Returns (None, None) if no task is selected or if the task (like Steps/Quiz) does not produce a chainable text result.
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