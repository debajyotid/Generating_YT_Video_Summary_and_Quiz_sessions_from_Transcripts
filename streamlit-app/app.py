"""
📘 Learn With AI — Modular YouTube Learning Assistant
==================================================

This project is a fully modular, state-driven Streamlit application that transforms YouTube videos into structured learning resources. It retrieves a video transcript, allows the user to select the transcript language, and enables a suite of AI-powered tasks such as translation, summarization, step-by-step guide generation, quiz creation, and audio narration. 
The system is designed for clarity, extensibility, and maintainability, using a clean separation between core logic, UI components, and state-driven orchestration.

This Streamlit application provides an interactive, modular workflow for transforming YouTube videos into structured learning resources. The system retrieves a video's transcript, allows the user to choose the transcript 
language (if multiple are available), and then enables a set of downstream AI-powered tasks such as translation, summarisation, step-by-step guide generation, quiz creation, and audio narration.

---------------------------------------------------------------------------
🏗️ Architecture
---------------------------------------------------------------------------
The design follows a hub-and-spoke architecture where the transcript acts as the central hub:

    TRANSCRIPT (hub) → Translation / Summarisation (Open Source & ChatGPT) / Steps (ChatGPT) / Quiz (ChatGPT) / Audio (TTS)

The transcript acts as the central shared resource. Once loaded, the user can trigger any of the available tasks independently or chain them together (e.g., summarise → translate summary → generate audio).

---------------------------------------------------------------------------
🎯 Core Objectives
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
5. Maintain modularity, readability, and extensibility through a clean separation of UI, logic, and model utilities.

---------------------------------------------------------------------------
🧱 Project Structure
---------------------------------------------------------------------------
    streamlit-app/
    │
    ├── app.py              # Main orchestrator
    │
    ├── core/               # Business Logic Layer
    │   ├── transcript.py
    │   ├── translate.py
    │   ├── summarization.py
    │   ├── gpt_utils.py
    │   └── audio.py
    │
    └── ui/                 # Presentation Layer
        ├── render_form.py
        ├── initial_task_selection.py
        └── followup_task.py

---------------------------------------------------------------------------
🧩 Module Overview
---------------------------------------------------------------------------

### 1. core/ — Business Logic Layer
---------------------------------------------------------------------------
- The application is organised into a set of modules under the 'core/' package, each responsible for a specific domain of functionality:
- These modules are stateless, testable, and contain all non-UI business logic.
    - **core.transcript**: Extracts video IDs and retrieves transcripts.
        - Provides transcript retrieval and language selection.
        - Supplies the central "hub" text used by all other tasks.
    - **core.translate**: Handles HuggingFace translation pipelines and text segmentation.
    - **core.summarization**: Provides open‑source summarisation using HuggingFace models.
    - **core.gpt_utils**: Initializes OpenAI client for GPT-based summaries, steps, and quizzes.
        - get_client(api_key)
        - gpt_summary(text)
        - gpt_steps(text)
        - gpt_quiz(text)
    - **core.audio**: Converts text to speech using OpenAI TTS.
		
### 2. ui/ — Presentation Layer
---------------------------------------------------------------------------
- This is a seperate 'ui/' module
- Streamlit components that read/write to st.session_state and call core functions.
    - **ui.render_form**: Handles URL input and transcript retrieval.
    - **ui.initial_task_selection**: Manages primary tasks (Summary, Quiz, etc.).
    - **ui.followup_task**: Handles secondary actions like translating summaries or downloading audio.

---------------------------------------------------------------------------
🔄 State-Driven Workflow
---------------------------------------------------------------------------
The UI is rendered based on st.session_state to ensure:
- Buttons remain persistent after interaction.
- Data persists across reruns.
- Tasks can be chained in any order.
- Predictable behavior on Streamlit Community Cloud.

---------------------------------------------------------------------------
🛠️ Extensibility
---------------------------------------------------------------------------

The modular structure allows new tasks to be added easily:
- Add a new function in a core module.
- Add a UI section that calls it.
- Optionally chain it with existing tasks.
- Update app.py to include the new component.

This architecture ensures the app remains maintainable, scalable, and easy to evolve as new AI capabilities or learning workflows are introduced.

---------------------------------------------------------------------------
📦 Installation & Deployment
---------------------------------------------------------------------------

Local Setup
---------------------------------------------------------------------------

#### Install dependencies
    pip install -r requirements.txt

#### Run the application
    streamlit run app.py

Deployment
---------------------------------------------------------------------------
Compatible with Streamlit Community Cloud, simply ensure that the **requirements.txt** includes:

    openai
    streamlit
    transformers
    youtube-transcript-api

"""
import streamlit as st

from ui.render_form import (ui_render_refresh_button, ui_initial_form_renderer)
from ui.initial_task_selection import ui_primary_task_section
from ui.followup_task import ui_followup_section

# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
def main():
    """
    The main entry point for the "Learn With AI" Streamlit application.

    Orchestrates the application flow:
    1.  **Configuration**: Sets page title and layout.
    2.  **State Management**: Renders a refresh button to reset session state.
    3.  **Step 1 (Transcript)**: Invokes `ui_initial_form_renderer` to load transcript via URL, upload, or manual input.
    4.  **Step 2 (Primary Task)**: Invokes `ui_primary_task_section` if a transcript is present.
    5.  **Step 3 (Follow-up)**: Invokes `ui_followup_section` if a summary is present.
    """

    st.set_page_config(page_title="Learn With AI", layout="wide")
    # Create a REFRESH button to reset the app state
    ui_render_refresh_button()

    st.title("🎓 Learn With AI — Modular YouTube Learning Assistant")

    # Step 1: Transcript (updates session_state.transcript / transcript_lang / video_id)
    ui_initial_form_renderer()

    # Step 2: Primary Task (updates session_state.summary / summary_lang)
    # Render Step 2 ONLY if transcript exists
    if st.session_state.get("transcript"):
        ui_primary_task_section()

    # Step 3: Follow-up Actions on summary (uses summary from session_state)
    # Render Step 3 ONLY if summary exists
    if st.session_state.get("summary"):
        ui_followup_section()

if __name__ == "__main__":
    main()