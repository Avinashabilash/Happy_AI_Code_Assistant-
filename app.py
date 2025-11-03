import streamlit as st
import requests
import json

# --- API Configuration ---
url = "http://localhost:11434/api/generate"  # 🔴 Change this to your remote endpoint if deploying
headers = {"Content-Type": "application/json"}

# --- Store Chat History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Happy Assistant", page_icon="🤖", layout="wide")

st.title("🤖 HAPPY ASSISTANT HERE")
st.markdown("###### Created by **Avinash** – your code-teaching AI assistant powered by Code Llama 💻")

# --- Sidebar Settings ---
st.sidebar.header("Settings ⚙️")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
model_name = st.sidebar.text_input("Model", "codehappy:7b")

# --- User Input ---
user_prompt = st.text_area("💬 Enter your Prompt:", height=150, placeholder="Ask your code question here...")

# --- Generate Button ---
if st.button("🚀 Generate Response"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt first!")
    else:
        st.session_state.history.append(user_prompt)
        final_prompt = "\n".join(st.session_state.history)

        data = {
            "model": model_name,
            "prompt": final_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }

        with st.spinner("Generating response... Please wait ⏳"):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))

                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("response", "No response found.")
                    st.session_state.history.append(reply)
                    st.text_area("🧠 Response:", value=reply, height=400)
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Connection Error: {e}")

# --- Show Chat History ---
if st.checkbox("Show Conversation History"):
    for i, msg in enumerate(st.session_state.history):
        st.markdown(f"**{('🧑‍💻 You' if i % 2 == 0 else '🤖 Happy')}:** {msg}")
