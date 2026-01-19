"""
Summarization Module.

This module provides functionality for summarizing text using local open-source models
via the Hugging Face `transformers` library. It includes:
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
def summarize_text(text, _summarizer, chunk_words=200):
    """
    Summarizes a long text by splitting it into word-based chunks and summarizing each chunk.

    Args:
        text (str): The input text to summarize.
        summarizer (transformers.Pipeline): The loaded summarization pipeline.
        chunk_words (int, optional): The number of words per chunk. Defaults to 200.

    Returns:
        str: The combined summary of all chunks.
    """
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_words]) for i in range(0, len(words), chunk_words)]
    summary = ""
    for chunk in chunks:
        result = _summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summary += result[0]["summary_text"] + " "
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