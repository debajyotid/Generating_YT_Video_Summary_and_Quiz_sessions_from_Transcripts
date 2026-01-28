"""
GPT Utilities Module

This module provides helper functions to interact with OpenAI's GPT models.
It includes functionality for:
1.  Initializing the OpenAI client.
2.  Summarizing long transcripts using a chunking strategy.
3.  Generating step-by-step instructions from text.
4.  Creating multiple-choice quizzes based on the provided content.

Dependencies:
    - openai: The official Python library for the OpenAI API.
"""
import streamlit as st
from openai import OpenAI
from openai import AuthenticationError

def ui_get_openai_client():
    """
    Manages the UI for OpenAI API key input and validation, returning a client.

    This function encapsulates the logic for:
    1.  Displaying a password input for the OpenAI API key.
    2.  Calling the core `get_client` function to validate the key.
    3.  Displaying success or error messages.
    4.  Storing the validated client and status in session state.
    5.  Triggering a rerun on successful validation to update the UI.

    Returns:
        openai.OpenAI | None: A validated OpenAI client instance if the key is
        valid, otherwise None. The UI is updated as a side effect.
    """
    # If key is already validated and client exists, return it.
    if st.session_state.get("apikey_valid") and st.session_state.get("openaiclient"):
        return st.session_state.openaiclient

    # Prompt for key.
    api_key = st.text_input("Enter your OpenAI API Key to use ChatGPT tasks.", type="password", key="api_key_input")

    # If a key is provided, attempt to validate it.
    if not api_key or api_key.strip() == "":
        st.session_state.apikey_valid = False
        st.session_state.openaiclient = None
        st.error(f"❌ No API key provided. Please enter a valid OpenAI API key.")
    else:
        if api_key:
            try:
                client = OpenAI(api_key=api_key)

                # The constructor doesn't validate the key, so we make a test call.
                client.models.list()
            
            except AuthenticationError:
                st.error(f"❌ Couldn't authorise provided key. Please check if your OpenAI API key is correct and has permissions.")
                st.session_state.apikey_valid = False                
            except Exception as e:
                st.error(f"❌ Error validating API key: {e}")
                st.session_state.apikey_valid = False

            st.success("✅ API key validated successfully. You can now run the task.")
            st.session_state.apikey_valid = True
            st.session_state.openaiclient = client
            st.session_state.openai_key = api_key  # Save the key for persistence
            st.rerun()

    return None    

def gpt_summary(client, transcript_text):
    """
    Generates a summary of the provided transcript text using GPT-4o-mini.

    Due to token limits, the text is split into chunks (approx 4000 characters),
    summarized individually, and then concatenated.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        transcript_text (str): The full text of the transcript to summarize.

    Returns:
        str: The concatenated summary of the transcript.
    """
    chunks = []
    # simple chunking
    while len(transcript_text) > 4000:
        chunks.append(transcript_text[:4000])
        transcript_text = transcript_text[4000:]
    chunks.append(transcript_text)

    summary = ""
    for chunk in chunks:
        response = client.chat.completions.create(
                                                    model="gpt-4o-mini",
                                                    messages=[
                                                                {"role": "system", "content": "You are a helpful assistant."},
                                                                {"role": "user", "content": f"{chunk}\n\nCreate a short concise summary."}
                                                            ],
                                                    max_tokens=250,
                                                    temperature=0.5
                                                )
        summary += response.choices[0].message.content.strip() + " "
    return summary.strip()

def gpt_steps(client, text):
    """
    Generates step-by-step instructions from the provided text using GPT-4o-mini.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        text (str): The source text to extract steps from.

    Returns:
        str: The generated steps formatted as a string.
    """
    response = client.chat.completions.create(
                                                model="gpt-4o-mini",
                                                messages=[
                                                            {"role": "system", "content": "You are a technical instructor."},
                                                            {"role": "user", "content": text},
                                                            {"role": "user", "content": "Generate steps to follow from the text."}
                                                        ]
                                            )
    return response.choices[0].message.content

def gpt_quiz(client, text):
    """
    Generates a 10-question multiple-choice quiz based on the provided text.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        text (str): The source text to generate the quiz from.

    Returns:
        str: The generated quiz questions and options.
    """
    response = client.chat.completions.create(
                                                model="gpt-4o-mini",
                                                messages=[
                                                            {"role": "system", "content": "You generate quiz questions."},
                                                            {"role": "user", "content": text},
                                                            {"role": "user", "content": "Generate 10 quiz questions with multiple choices."}
                                                        ]
                                            )
    return response.choices[0].message.content

def gpt_audio(client, text):
    """
    Generates speech audio from text using OpenAI's Text-to-Speech API.

    This function uses the specified OpenAI client to convert the input text
    into audio using the 'gpt-4o-mini-tts' model and 'alloy' voice.
    The result is cached by Streamlit to avoid redundant API calls.

    Args:
        text (str): The text content to convert to speech.
        client (openai.OpenAI): An initialized OpenAI client instance.

    Returns:
        bytes: The binary content of the generated audio file.
    """
    speech = client.audio.speech.create(
                                            model="gpt-4o-mini-tts",
                                            voice="alloy",
                                            input=text
                                        )
    return speech.read()