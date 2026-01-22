"""
GPT Utilities Module.

This module provides helper functions to interact with OpenAI's GPT models.
It includes functionality for:
1.  Initializing the OpenAI client.
2.  Summarizing long transcripts using a chunking strategy.
3.  Generating step-by-step instructions from text.
4.  Creating multiple-choice quizzes based on the provided content.

Dependencies:
    - openai: The official Python library for the OpenAI API.
"""
from openai import OpenAI

def get_client(api_key):
    """
    Initializes and returns an OpenAI client using the provided API key.

    Args:
        api_key (str): The OpenAI API key.

    Returns:
        openai.OpenAI: An instance of the OpenAI client.
    """
    if not api_key or api_key.strip() == "":
        return None, "No API key provided. Please enter a valid OpenAI API key."

    try:
        client = OpenAI(api_key=api_key)
        return client, None
    
    except Exception as e:
        return None, f"Invalid or unauthorized API key. Please enter a valid key. ({e})"
    

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