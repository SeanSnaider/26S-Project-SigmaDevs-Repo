import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Dashboard Layouts")
st.subheader("View dashboard layout configurations")

st.write(f"### Hi, {st.session_state['first_name']}.")

col1, col2 = st.columns([1, 3])

with col1:
    layout_id = st.number_input(
        "Layout ID",
        min_value=1,
        value=9001,
        step=1
    )
with col2:
    st.write("")
    st.write("")
    load = st.button(
        "Load Layout Data",
        type="primary",
        use_container_width=True
    )

if load:
    try:
        response = requests.get(f"http://web-api:4000/dashboardlayouts/{layout_id}")
        if response.status_code != 200:
            st.error("Layout not found / API Error.")
        else:
            data = response.json()
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Layout ID", data['layout_id'])
            col2.markdown("**Layout Name:**")
            col2.markdown(f"{data['name']}")
            col3, col4 = st.columns(2)
            col3.markdown("**Source:**")
            col3.markdown(f"{data['source']}")
            col4.markdown("**Layout Config:**")
            col4.markdown(f"{data['layout_dash']}")

            st.divider()
            st.subheader("Layout Details")

            df = pd.DataFrame([data])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()

    except Exception as e:
        logger.error(f"Error loading layout: {e}")
        st.error("Failed to load layout data.")
