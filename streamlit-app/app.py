"""
Learn With AI — Modular YouTube Learning Assistant
==================================================

This Streamlit application provides an interactive, modular workflow for transforming YouTube videos into structured learning resources. The system retrieves a video's transcript, allows the user to choose the transcript language (if multiple are available), and then enables a set of downstream AI-powered tasks such as translation, summarisation, step-by-step guide generation, quiz creation, and audio narration.

The design follows a hub-and-spoke architecture:

    TRANSCRIPT (hub) → Translation / Summarisation / Steps / Quiz / Audio (spokes)

The transcript acts as the central shared resource. Once loaded, the user can trigger any of the available tasks independently or chain them together (e.g., summarise → translate summary → generate audio).

---------------------------------------------------------------------------
Core Objectives
---------------------------------------------------------------------------

1. Provide a flexible, user-driven workflow for learning from YouTube videos.
2. Support multiple transcript languages when available.
3. Allow translation into a predefined set of target languages.
4. Enable multiple downstream tasks:
       - Translation of transcript or summary
       - Summarisation (open-source or ChatGPT)
       - Step-by-step guide generation (ChatGPT)
       - Quiz generation (ChatGPT)
       - Audio narration of summaries (TTS)
5. Maintain modularity, readability, and extensibility through a clean    separation of UI, logic, and model utilities.

---------------------------------------------------------------------------
Module Overview and How They Tie Together
---------------------------------------------------------------------------

The application is organised into a set of modules under the 'core/' package, each responsible for a specific domain of functionality:

1. core.transcript
   - list_available_transcripts(video_id)
   - get_transcript(video_id, language_code)
   - Provides transcript retrieval and language selection.
   - Supplies the central "hub" text used by all other tasks.

2. core.translation
   - PREDEFINED_LANGS (mapping of human labels → language codes)
   - get_translation_pipeline(src_lang, tgt_lang)
   - translate_text(text, translator)
   - Handles translation of transcript or summary using dynamic model selection.

3. core.summarization
   - load_summarizer()
   - summarize_text(text, summarizer)
   - Provides open‑source summarisation using HuggingFace models.

4. core.gpt_utils
   - get_client(api_key)
   - gpt_summary(text)
   - gpt_steps(text)
   - gpt_quiz(text)
   - Provides ChatGPT-based summarisation, step extraction, and quiz generation.

5. core.audio
   - generate_audio(text, client)
   - Converts summaries into spoken audio using TTS.

There is also a seperate 'ui/' module that organises the Streamlit interface into three main sections:

1. ui.render_form
   - ui_initial_form_renderer(): Handles YouTube URL input, transcript language selection, and retrieval.
       - User enters a YouTube URL.
       - Available transcript languages are listed.
       - User selects a language and retrieves the transcript.
       - The transcript is stored in session state.
2. ui.initial_task_selection
   - ui_primary_task_section(transcript, transcript_lang, openai_key): Manages primary task selection and execution (translation, summarisation, steps, quiz).
        - User chooses one of the main tasks:
            Translation
            Summarisation (Open Source)
            Summarisation (ChatGPT)
            Steps (ChatGPT)
            Quiz (ChatGPT)
        - The corresponding core module function is invoked.
        - Outputs are displayed and optionally stored for follow-up tasks.
3. ui.followup_task
   - ui_followup_section(summary, summary_lang, openai_key): Manages follow-up actions on the summary (translation, audio generation, download).
        - If a summary exists, the user can:
            Translate the summary
            Generate audio narration
            Download the summary
        - These actions use the same translation and audio modules.
---------------------------------------------------------------------------
Extensibility
---------------------------------------------------------------------------

The modular structure allows new tasks to be added easily:
    - Add a new function in a core module.
    - Add a UI section that calls it.
    - Optionally chain it with existing tasks.

This architecture ensures the app remains maintainable, scalable, and easy to evolve as new AI capabilities or learning workflows are introduced.

"""
import streamlit as st

from ui.render_form import ui_initial_form_renderer
from ui.initial_task_selection import ui_primary_task_section
from ui.followup_task import ui_followup_section

# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
def main():
    """
    The main function of the Streamlit application. It serves as the entry point for the "Learn With AI" Streamlit application. It orchestrates the application flow by invoking specific UI sections defined in the 'ui' module.

    It performs the following actions:
    1.  Configures the Streamlit page settings (title, layout).
    2.  Prompts the user for an OpenAI API key.
    3.  Invokes `ui_initial_form_renderer` to handle YouTube URL input and transcript retrieval.
    4.  Invokes `ui_primary_task_section` to process the transcript (e.g., summarize, quiz).
    5.  Invokes `ui_followup_section` to handle post-processing actions (e.g., audio generation).
    """
    st.set_page_config(page_title="Learn With AI", layout="wide")
    st.title("🎓 Learn With AI — Modular YouTube Learning Assistant")

    openai_key = st.text_input("Enter your OpenAI API Key", type="password")

    # Step 1: Transcript
    transcript, transcript_lang, video_id = ui_initial_form_renderer()

    # Step 2: Primary Task
    summary, summary_lang = ui_primary_task_section(transcript, transcript_lang, openai_key)

    # Step 3: Follow-up Actions
    ui_followup_section(summary, summary_lang, openai_key)

# ---------------------------------------------------------
# Streamlit entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()