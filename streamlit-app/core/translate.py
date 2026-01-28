"""
Translation Module.

This module provides functionality for translating text between supported languages
using Hugging Face's 'transformers' library and pre-trained models (Helsinki-NLP).
It includes:
1.  Configuration for supported language pairs and models.
2.  Loading and caching translation pipelines.
3.  Translating text by splitting it into manageable segments.

Dependencies:
    - transformers: For the translation pipeline.
    - streamlit: For caching resources and data.
"""
import streamlit as st
from transformers import pipeline

# Supported translation directions and corresponding models
# You can expand this map as needed
TRANSLATION_MODELS = {
                        ("en", "es"): "Helsinki-NLP/opus-mt-en-es",
                        ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
                        ("en", "de"): "Helsinki-NLP/opus-mt-en-de",
                        ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
                        ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
                        ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
                    }

PREDEFINED_LANGS = {
                        "English": "en",
                        "Spanish": "es",
                        "French": "fr",
                        "German": "de",
                    }

@st.cache_resource(show_spinner=False)
def get_translation_pipeline(src_lang, tgt_lang):
    """
    Retrieves and caches the translation pipeline for a specific source and target language pair.

    Args:
        src_lang (str): The source language code (e.g., 'en').
        tgt_lang (str): The target language code (e.g., 'es').

    Returns:
        transformers.Pipeline: The loaded translation pipeline.

    Raises:
        ValueError: If the requested language pair is not supported in 'TRANSLATION_MODELS'ß.
    """
    key = (src_lang, tgt_lang)
    if key not in TRANSLATION_MODELS:
        raise ValueError(f"No model configured for {src_lang} → {tgt_lang}")
    model_name = TRANSLATION_MODELS[key]
    return pipeline("translation", model=model_name)

@st.cache_data(show_spinner=False)
def translate_text(translator, text, max_length=512):
    """
    Translates a long text string using the provided translator pipeline.

    The text is split into segments to fit within the model's maximum sequence length. 
    Includes a progress bar and error handling for individual segments.

    Args:
        translator (transformers.Pipeline): The loaded translation pipeline.
        text (str): The input text to translate.
        max_length (int, optional): The maximum character length for each segment. Defaults to 512.

    Returns:
        str: The concatenated translated text.

    Raises:
        ValueError: If translation fails for all text segments.
    """

    segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    progress = st.progress(0)
    total = len(segments)

    translated = ""

    for i, seg in enumerate(segments):
        try:
            translated += translator(seg)[0]["translation_text"]
        except Exception as e:
            st.warning(f"Skipping segment {i+1} due to translation error: {e}")
        progress.progress((i+1)/total)
    
    if not translated:
        raise ValueError("Translation failed for all text segments.")

    return translated