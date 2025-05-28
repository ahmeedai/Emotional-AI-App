import streamlit as st
import requests

# Streamlit UI setup
st.set_page_config(page_title="Emotional AI", layout="centered")
st.title("🧠 Emotional AI")
st.write("Tell me how you're feeling. I'm here to support you ❤️")

# Load Gemini API key
API_KEY = st.secrets["GEMINI_API_KEY"]
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("How are you feeling today?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare payload
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"You are a caring emotional AI. Respond supportively to this:\n\n{user_input}"}]
            }
        ]
    }

    # Request to Gemini API
    try:
        res = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=data)
        if res.status_code == 200:
            reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = f"Error: {res.status_code} - {res.text}"
    except Exception as e:
        reply = f"Error: {e}"

    # Show assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
