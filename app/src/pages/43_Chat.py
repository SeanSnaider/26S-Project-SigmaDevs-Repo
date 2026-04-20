import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Portfolio Assistant")
st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("Ask me anything about your portfolio and investments.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about your positions...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res = requests.post("http://web-api:4000/chat/", json={"message": prompt})
            data = res.json()
            if res.status_code == 503:
                reply = "API key not connected. Add your GEMINI_API_KEY to api/.env and restart the container."
            elif res.status_code != 200:
                reply = f"Error: {data.get('error', 'Something went wrong.')}"
            else:
                reply = data.get("response", "No response.")
        except Exception as e:
            logger.error(f"Chat error: {e}")
            reply = "Failed to connect to the assistant."

        st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
