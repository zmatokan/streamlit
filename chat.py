import requests
import streamlit as st
import json

st.title("Custom Chatbot")

# Define your custom API URL
API_URL = "http://192.168.20.70:8080/chat"

# Function to send a message to the custom API and get the response
def get_bot_response(user_message):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "query": user_message,
        "stream": False  # Adjust if needed by your API
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            json_response = response.json()
            # Extract the content from the response
            return json_response.get("response", {}).get("content", "Sorry, I didn't get that.")
        else:
            return f"Error: Unable to contact the backend. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new messages
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from custom API
    bot_response = get_bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)