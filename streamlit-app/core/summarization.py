"""
Summarization Module.

This module provides functionality for summarizing text using local open-source models
via the Hugging Face 'transformers' library. It includes:
1.  Loading the summarization pipeline (cached).
2.  Summarizing long text by splitting it into chunks.
3.  Utility for splitting text.

Dependencies:
    - transformers: For the summarization pipeline.
    - streamlit: For caching resources and data.
"""
import textwrap
import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=False)
def load_summarizer():
    """
    Loads and caches the summarization pipeline using the 'facebook/bart-large-cnn' model.

    Returns:
        transformers.Pipeline: The loaded summarization pipeline.
    """
    return pipeline("summarization", model="facebook/bart-large-cnn")

@st.cache_data(show_spinner=False)
def summarize_text(summarizer, text, chunk_words=200):
    """
    Summarizes a long text by splitting it into word-based chunks and summarizing each chunk.

    Includes a progress bar and error handling for individual chunks to ensure partial success
    if specific chunks fail.

    Args:
        summarizer (transformers.Pipeline): The loaded summarization pipeline.
        text (str): The input text to summarize.
        chunk_words (int, optional): The number of words per chunk. Defaults to 200.

    Returns:
        str: The combined summary of all chunks.

    Raises:
        ValueError: If summarization fails for all text chunks.
    """
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_words]) for i in range(0, len(words), chunk_words)]
    summary = ""
    progress = st.progress(0)
    total = len(chunks)
    
    for i, chunk in enumerate(chunks):
        try:
            result = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
            summary += result[0]["summary_text"] + " "
        except Exception as e:
            st.warning(f"Skipping chunk {i+1} due to summarization error: {e}")
        progress.progress((i+1)/total)

    if not summary:
        raise ValueError("Summarization failed for all text chunks.")

    return summary.strip()

def split_text_into_chunks(text, max_chunk_size=4000):
    """
    Splits a text string into a list of strings, each with a maximum width.

    Args:
        text (str): The input text.
        max_chunk_size (int, optional): The maximum number of characters per chunk. Defaults to 4000.

    Returns:
        list[str]: A list of text chunks.
    """
    return textwrap.wrap(text, max_chunk_size)