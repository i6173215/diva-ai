import streamlit as st
import requests
import dotenv
import os
import logging

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)

# Load environment variables from a .env file
dotenv.load_dotenv()
HF_KEY = os.getenv("HF_KEY")
API_URL = os.getenv("API_URL")

def diva_query(messages):
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
        "user_id": "user321"
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {HF_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=2500)
    logging.info("Received response from diva: %s", response.json())
    return response.json()

def display_messages(messages):
    """
    Display messages in the chat interface.

    Args:
        messages (list): List of messages to display.
    """
    logging.info("Displaying messages: %s", messages)
    for msg in messages:
        avatar = "\U0001F5E8" if msg["role"] == "user" else "\U0001F471"
        st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

def main():
    logging.info("Starting Streamlit app")
    # Streamlit app title and caption
    st.title("💬 DIVA")
    st.caption("AI Chat room")

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
        st.chat_message("user", avatar="\U0001F5E8").write(prompt)

        # Get response from diva
        response = diva_query(st.session_state.messages)

        # Extract and display diva response
        if "answer" in response:
            msg = response["answer"]
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant", avatar="\U0001F471").write(msg)
            logging.info("Diva response displayed: %s", msg)
        else:
            st.error("[ERROR] The response did not contain an answer.")
            logging.error("The response did not contain an answer: %s", response)

if __name__ == "__main__":
    main()