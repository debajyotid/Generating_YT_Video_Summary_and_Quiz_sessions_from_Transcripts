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
- Predictable behavior on Streamlit (including Community Cloud) & Docker.

Key state variables include:
    session_state.youtube_url
    session_state.video_id
    session_state.transcript
    session_state.transcript_lang
    session_state.transcript_options_loaded
    session_state.summary
    session_state.summary_lang
    session_state.openai_key

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
This project supports **three** deployment modes.

🚀 1. Deploy on Streamlit Community Cloud
            1. Push your repo to GitHub
            2. Go to https://streamlit.io/cloud
            3. Create a new app
            4. Set the main file to:
                    streamlit-app/app.py
            5. Ensure requirements.txt includes:
                        openai
                        streamlit
                        transformers
                        youtube-transcript-api==1.0.3
            6. This step is already completed and the app is available at **https://learn-from-youtube-with-ai.streamlit.app/**
                        
🐳 2. Deploy via Docker (Local or Cloud)
    - The repo already contains the below files:
        - Dockerfile 
        - docker-compose.yml
    - Simply clone the repo locally and run the below commands:
        - run locally
            docker-compose up --build
        - Access the app at:
            http://localhost:8501
        - Stop the container
            docker-compose down
        
☁️ 3. Deploy Docker Image to Cloud Platforms
    -  AWS ECS / Fargate
        1. Build and push image to ECR
        2. Create ECS service
        3. Expose port 8501
        4. Add environment variable OPENAI_API_KEY
    - Azure Container Apps
        1. Push image to Azure Container Registry
        2. Create Container App
        3. Configure ingress on port 8501
        4. Add environment variables
    - Google Cloud Run
        1. Build and push image to Artifact Registry
        2. Deploy to Cloud Run
        3. Allow unauthenticated access (optional)
        4. Set environment variables

Cloud Run is often the easiest option.

---------------------------------------------------------------------------
📜 License
Choose a license (MIT recommended) and include it here.
---------------------------------------------------------------------------

---------------------------------------------------------------------------
🙌 Acknowledgements
---------------------------------------------------------------------------
    - HuggingFace Transformers
    - OpenAI API
    - youtube-transcript-api
    - Streamlit


