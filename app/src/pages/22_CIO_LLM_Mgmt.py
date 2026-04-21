import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = "http://web-api:4000"

st.title("LLM Management - PortIQ")

# ── Recent call history ───────────────────────────────────────────────────────
st.write("### Recent LLM Call History")

try:
    resp = requests.get(f"{BASE_URL}/llm/calls")
    if resp.status_code == 200:
        logs = resp.json()
        if logs:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No LLM call logs found.")
    else:
        st.warning("Could not retrieve LLM call logs.")
except Exception as e:
    st.error(f"Error fetching LLM call logs: {e}")

