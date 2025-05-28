import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="Emotional AI", layout="centered")
st.title("🧠 Emotional AI")
st.markdown("Tell me how you're feeling. I'm here to support you ❤️")

# Load your Gemini API key from secrets
api_key = st.secrets["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

# Store messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an emotional AI. You listen to users and give kind, supportive, and helpful responses based on their feelings."}
    ]

# Show previous messages
for msg in st.session_state.chat_history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input box
user_input = st.chat_input("How are you feeling today?")
if user_input:
    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare data for Gemini
    data = {
        "contents": [
            {
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            }
            for msg in st.session_state.chat_history
            if msg["role"] in {"user", "assistant"}
        ]
    }

    # Send request to Gemini API
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=data
        )
        if response.status_code == 200:
            reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = f"⚠️ Error {response.status_code}: {response.text}"
    except Exception as e:
        reply = f"❌ Unexpected error: {e}"

    # Show AI response
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
