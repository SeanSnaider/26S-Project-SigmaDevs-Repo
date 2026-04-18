import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Portfolio Performance")
st.subheader("Monitor portfolio value and profit & loss")

st.write(f"### Hi, {st.session_state['first_name']}.")

col1, col2 = st.columns([1,3])

with col1: 
    portfolio_id = st.number_input(
        "Portfolio ID",
        min_value = 1,
        value = 101,
        step=1
    )
with col2: 
    st.write("")
    st.write("")
    load = st.button(
        "Load Portfolio Data",
        type = "primary",
        use_container_width = True
    )

if load:
    try:
        response = requests.get(f"http://web-api:4000/portfolios/{portfolio_id}")
        if response.status_code != 200:
            st.error("Portfolio not found/API Error.")
        else:
            data = response.json()
            st.divider()
            col1,col2 = st.columns(2)
            col1.metric("Portfolio ID", data['portfolio_id'])
            col2.markdown("**Portfolio Name:**")
            col2.markdown(f"{data['portfolio_name']}")
            col3,col4=st.columns(2)
            col3.metric("Total Value", f"${data['total_value']:,.2f}")
            col4.markdown("**Confidence:**")
            col4.markdown(f"{data['confidence']}")
            col5, col6 = st.columns(2)
            col5.metric("Daily P&L",f"${data['total_daily_PNL']:,.2f}")
            col6.metric("Cumulative P&L", f"${data['total_cumulative_PNL']:,.2f}")

            st.divider()
            st.subheader("Portfolio Details")

            df= pd.DataFrame([data])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.divider()




    except Exception as e:
        logger.error(f"Error loading portfolio: {e}")
        st.error("Failed to load portfolio data.")
