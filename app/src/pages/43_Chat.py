# Based on: https://medium.com/@gayathri.s.de/building-a-chatbot-using-gemini-api-and-streamlit-34292b38fc57

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


def map_role(role):
    return "assistant" if role == "model" else role


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about your positions...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = [
        {"role": m["role"], "parts": [m["content"]]}
        for m in st.session_state.messages[:-1]
    ]

    with st.chat_message("assistant"):
        try:
            res = requests.post(
                "http://web-api:4000/chat/",
                json={"message": prompt, "history": history}
            )
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
        st.session_state.messages.append({"role": "model", "content": reply})
