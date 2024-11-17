import streamlit as st
import requests
import os
import logging
from typing import List, Dict, Any

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)

# Load environment variables
HF_KEY = os.getenv("HF_KEY")
API_URL = os.getenv("API_URL")

# Constants for icons
ICON_USER = "\U0001f5e8"
ICON_ASSISTANT = "\U0001f469"
ICON_TITLE = "\U0001f4bb"  # laptop

# Streamlit page configuration
st.set_page_config(
    page_title="DIVA AI",
    page_icon="assets/logo-3.jpg",
    layout="wide",
    initial_sidebar_state="auto",
)

def diva_query(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Send a query to the diva and return the response.

    Args:
        messages (list): List of messages to send to the diva.

    Returns:
        dict: JSON response from the diva.
    """
    logging.info("Sending query to diva with messages: %s", messages)
    payload = {
        "messages": messages,
        "sk": [1, 2, 3, 4],
        "iv": [5, 6, 7, 8],
        "user_id": "user321",
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {HF_KEY}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=500)
        response.raise_for_status()
        logging.info("Received response from diva: %s", response.json())
        return response.json()
    except requests.RequestException as e:
        # block url error
        logging.error("Request failed. 503 or OOM")
        return {"error": "Сервер недоступен.\n1) Попробуйте позже (Перезагрузка сервера 10-15 минут)\n2) Попробуйте уменьшить длину запроса (количество слов)"}

def display_messages(messages: List[Dict[str, str]]) -> None:
    """
    Display messages in the chat interface.

    Args:
        messages (list): List of messages to display.
    """
    logging.info("Displaying messages: %s", messages)
    for msg in messages:
        avatar = ICON_USER if msg["role"] == "user" else ICON_ASSISTANT
        st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

def main() -> None:
    """
    Main function to run the Streamlit app for DIVA AI Chat Room.

    This function initializes the Streamlit app, sets up the title and caption,
    manages the session state for messages, displays previous messages, handles
    new user input, and processes responses from the DIVA AI.
    """
    logging.info("Starting Streamlit app")

    # Streamlit app title and caption
    st.markdown(
        f"<h3 style='text-align: center;'>{ICON_TITLE} DIVA AI Chat Room {ICON_TITLE}</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h6 style='text-align: center;'>[2024.11 | Версия 0.1 | Только для тестирования]</h6>",
        unsafe_allow_html=True,
    )

    # Initialize session state for messages if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logging.info("Initialized session state for messages")

    # Display previous messages
    display_messages(st.session_state.messages)

    # Handle new user input
    if prompt := st.chat_input():
        logging.info("User input received: %s", prompt)
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        st.chat_message("user", avatar=ICON_USER).write(prompt)

        # Get response from diva
        response = diva_query(st.session_state.messages)

        # Extract and display diva response
        if "answer" in response:
            msg = response["answer"]
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant", avatar=ICON_ASSISTANT).write(msg)
            logging.info("Diva response displayed: %s", msg)
        else:
            # Handle errors
            error_message = response.get("error", "Unknown error occurred.")
            st.error(f"[Ошибка] {error_message}")
            logging.error("Error in response: %s", error_message)

if __name__ == "__main__":
    main()
