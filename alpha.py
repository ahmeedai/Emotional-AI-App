import streamlit as st
import requests

# Set up the page
st.set_page_config(page_title="Emotional AI", layout="centered")
st.title("🧠 Emotional AI")
st.write("Tell me how you're feeling. I'm here to support you ❤️")

# Your Gemini API key (stored securely in Streamlit secrets)
API_KEY = st.secrets["GEMINI_API_KEY"]
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent?key={API_KEY}"

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("How are you feeling today?")
if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create request for Gemini
    prompt = [
        {"role": "system", "parts": [{"text": "You are a caring emotional AI. Respond with empathy and support."}]},
        {"role": "user", "parts": [{"text": user_input}]}
    ]
    data = {"contents": prompt}

    try:
        res = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=data)
        if res.status_code == 200:
            reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = f"Error: {res.status_code} - {res.text}"
    except Exception as e:
        reply = f"Error: {e}"

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
