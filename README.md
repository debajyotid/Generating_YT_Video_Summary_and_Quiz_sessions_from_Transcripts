📘 Learn With AI — Modular YouTube Learning Assistant
==================================================
A Streamlit + OpenAI + HuggingFace application for summarizing, translating, and learning from YouTube videos
---------------------------------------------------------------------------

This project began as a Jupyter notebook exploring how to extract YouTube transcripts and generate summaries, step‑by‑step guides, and quizzes using open‑source models and ChatGPT. It has since evolved into a **fully modular, state‑driven Streamlit application** with Docker support and multiple execution paths.

The app transforms YouTube videos into structured learning resources by:
- Fetching transcripts (with multi‑language support)
- Summarizing content (open‑source or ChatGPT)
- Translating transcripts or summaries
- Generating step‑by‑step instructions
- Creating quizzes
- Producing audio narration of summaries

The system is built for clarity, maintainability, and extensibility,  using a clean separation between core logic, UI components, and state-driven orchestration.

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
🏗️ Architecture
---------------------------------------------------------------------------
The design follows a **hub-and-spoke** architecture where the transcript acts as the central hub:

    TRANSCRIPT (hub)
    ├── Translation
	├── Summarisation (Open Source)
	├── Summarisation (ChatGPT)
	├── Steps (ChatGPT)
	├── Quiz (ChatGPT)
	└── Audio Narration (TTS)

The transcript acts as the central shared resource. Once loaded, the user can trigger any of the available tasks independently or chain them together (e.g., summarise → translate summary → generate audio).

---------------------------------------------------------------------------
🧱 Project Structure
---------------------------------------------------------------------------

	streamlit-app/
	│
	├── app.py                     # Main orchestrator
	│
	├── core/                      # Business Logic Layer
	│   ├── transcript.py
	│   ├── translate.py
	│   ├── summarization.py
	│   ├── gpt_utils.py
	│   └── audio.py
	│
	├── ui/                        # Presentation Layer
	│   ├── render_form.py
	│   ├── initial_task_selection.py
	│   └── followup_task.py
	│
	├── learn_with_ai.py           # Original notebook exported as .py
	└── learn_with_ai.ipynb        # Original Jupyter notebook

---------------------------------------------------------------------------
🧩 Module Overview
---------------------------------------------------------------------------
										### Streamlit App
						
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
										### Jupyter Notebooks

### 3. learn_with_ai.ipynb / learn_with_ai.py
The original notebook version of the project, preserved for experimentation, education, and reproducibility.

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

This project supports multiple deployment modes.

### 1. Run the Streamlit App Locally
---------------------------------------------------------------------------

#### Install dependencies
    pip install -r requirements.txt

#### Run the application
    streamlit run app.py

Run the Jupyter Notebook Version
---------------------------------------------------------------------------

The notebook version (learn_with_ai.ipynb) contains the full workflow:
	- Transcript extraction
	- Translation
	- Summarisation
	- GPT‑based steps and quiz generation

#### Run locally
	jupyter notebook learn_with_ai.ipynb
	
### 2. Run the Python Script Version
---------------------------------------------------------------------------

The notebook is also exported as a standalone script:
	python streamlit-app/learn_with_ai.py

This is useful for:
	- CLI workflows
	- Batch processing
	- Integrating into other systems

### 3. Deploy Using Docker (Local or Cloud)
---------------------------------------------------------------------------

- Build the image

		docker build -t learn-with-ai ./streamlit-app

- Run the container

		docker run -p 8501:8501 learn-with-ai

- Access the app at:

		http://localhost:8501

---------------------------------------------------------------------------
☁️ Cloud Deployment Options
---------------------------------------------------------------------------

### Streamlit Community Cloud
---------------------------------------------------------------------------

1. Push repo to GitHub
2. Create a new app
3. Set main file to:

		streamlit-app/app.py
   
5. Ensure requirements.txt includes:
   
		- openai
   		- streamlit
		- transformers
		- youtube-transcript-api==1.0.3

### Deploy Docker Image to Cloud Platforms
---------------------------------------------------------------------------

#### Google Cloud Run (easiest)

1. Build and push image to Artifact Registry
2. Deploy to Cloud Run
3. Allow unauthenticated access
4. Set OPENAI_API_KEY

#### AWS ECS / Fargate

1. Push image to ECR
2. Create ECS service
3. Expose port 8501
4. Add environment variables
	
#### Azure Container Apps

1. Push image to ACR
2. Create Container App
3. Configure ingress
4. Add environment variables

---------------------------------------------------------------------------
📜 License
---------------------------------------------------------------------------

This project is licensed under the MIT License, a permissive open‑source license that allows:
• Commercial use
• Modification
• Distribution
• Private use
See the LICENSE file for details.

---------------------------------------------------------------------------
🙌 Acknowledgements
---------------------------------------------------------------------------
    - HuggingFace Transformers
    - OpenAI API
    - youtube-transcript-api
    - Streamlit


