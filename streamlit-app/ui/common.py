"""
UI Component: Common UI Helpers.

This module provides common UI helper functions that can be shared across
different UI sections to avoid code duplication, particularly for handling
the OpenAI API key and client initialization.
"""
import streamlit as st
from core.gpt_utils import get_client

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
    if api_key:
        client, err = get_client(api_key)
        if err:
            st.error(f"❌ {err}")
            st.session_state.apikey_valid = False
        else:
            st.success("✅ API key validated successfully. You can now run the task.")
            st.session_state.apikey_valid = True
            st.session_state.openaiclient = client
            st.session_state.openai_key = api_key  # Save the key for persistence
            st.rerun()

    return None

def ui_render_refresh_button():
    """
    Renders a 'REFRESH' button to clear session state and reset the app.
    Displays a success message upon successful reset.
    """
    # Check if the app was just reset and display a success message
    if st.session_state.get("reset_success"):
        st.success("✅ App has been reset successfully.")
        del st.session_state["reset_success"]

    if st.button("REFRESH", type="primary", help="Clear all data and reset"):
        st.session_state.clear()
        st.session_state.reset_success = True
        st.rerun()