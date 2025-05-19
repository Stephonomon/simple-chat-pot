import streamlit as st
import requests
from openai import OpenAI

BACKEND_URL = "https://snp-vite-backend.onrender.com"

def check_backend():
    try:
        response = requests.get(BACKEND_URL, timeout=7)
        if response.status_code == 200:
            return True, "Backend available!"
        else:
            return False, f"Backend responded with status code: {response.status_code}"
    except Exception as e:
        return False, f"Failed to connect to backend: {e}"

# Run the backend test on load
with st.spinner("Checking backend server..."):
    backend_ok, backend_message = check_backend()

if backend_ok:
    st.success(backend_message)
else:
    st.error(backend_message)
    st.stop()  # Stop app if backend unavailable

st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

openai_api_key = st.secrets["OPENAI_API_KEY"]

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
