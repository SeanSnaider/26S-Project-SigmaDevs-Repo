import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Trading Logs")

st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("View, create, update, and delete trade, records.")

tab1, tab2, tab3, tab4 = st.tabs([
    'All Trades',
    'Lookup Trade',
    'Create / Update Trade',
    'Delete Trade'
])

# All trades
with tab1:
    st.subheader("Recent Trades")
    if st.button("Load All Trades", use_container_width=True):
        try:
            trades_res = requests.get("http://web-api:4000/trades")
            trades_data = trades_res.json()
            if trades_res.status_code !=200:
                st.error(f"could not load trades: {trades_data}")
            else:
                trades_df = pd.DataFrame(trades_data)

                if len(trades_df) >0:
                    if "price" in trades_df.columns:
                        trades_df['price'] = pd.to_numeric(trades_df['price'], errors='coerce').round(2)
                    if 'quantity' in trades_df.columns:
                        trades_df['quantity'] = pd.to_numeric(trades_df['quantity'],errors='coerce').round(2)
                    st.dataframe(trades_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No Trades Found!")
        except Exception as e:
            logger.error(f"Error loading trades: {e}")
            st.error("Failed to load trades.")

with tab2:
    st.subheader("Lookup One Trade")
    lookup_trade_id = st.number_input("Trade ID", min_value=1, value=15001, step=1, key="lookup_trade")
    if st.button("Get Trade Details", use_container_width=True):
        try:
            trade_res=requests.get(f"http://web-api:4000/trades/{lookup_trade_id}")
            trade_data=trade_res.json()
            if trade_res.status_code !=200:
                st.error(f"could not load trade: {trade_data}")
            else:
                trade_df = pd.DataFrame([trade_data])
                st.dataframe(trade_df, use_container_width=True, hide_index=True)
        except Exception as e:
            logger.error(f"Error loading one trade: {e}")
            st.error("Failed to load trade details.")





with tab4:
    st.subheader("Delete Trade")
    delete_trade_id = st.number_input("Trade ID to Delete", min_value=1, value=15001, step=1, key="delete_trade")
    if st.button("Delete Trade", use_container_width=True):
        try:
            delete_res=requests.delete(f"http://web-api:4000/trades/{delete_trade_id}")
            delete_data=delete_res.json()
            if delete_res.status_code !=200:
                st.success(f"Trade deleted successfully.")
            else:
                st.error(f"Failed to delete trade:{delete_data}")
        except Exception as e:
            logger.error(f"Error deleting trade: {e}")
            st.error("Failed to delete trade details.")
