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

with tab3:
    st.subheader("Create New Trade")

    with st.form("create_trade_form"):
        c1, c2 = st.columns(2)

        with c1:
            create_trade_id = st.number_input("New Trade ID", min_value=1, value=20001, step=1)
            create_trade_type = st.selectbox("Trade Type", ["BUY", "SELL"])

        with c2:
            create_quantity = st.number_input("Quantity", min_value=0.0, value=10.0, step=1.0)
            create_price = st.number_input("Price", min_value=0.0, value=100.00, step=0.01)
            create_trade_asset = st.number_input("Asset ID", min_value=1, value=13001, step=1)

        create_submit = st.form_submit_button("Create Trade")

        if create_submit:
            payload = {
                "trade_type": create_trade_type,
                "quantity": float(create_quantity),
                "price": float(create_price),
                "trade_id": int(create_trade_id),
                "trade_asset": int(create_trade_asset)
            }

            try:
                create_res = requests.post("http://web-api:4000/trades/", json=payload)
                create_data = create_res.json()

                if create_res.status_code == 201:
                    st.success("Trade created successfully.")
                else:
                    st.error(f"Failed to create trade: {create_data}")

            except Exception as e:
                logger.error(f"Error creating trade: {e}")
                st.error("Failed to create trade.")

    st.divider()
    st.subheader("Update Existing Trade")

    with st.form("update_trade_form"):
        u1, u2 = st.columns(2)

        with u1:
            update_trade_id = st.number_input("Trade ID to Update", min_value=1, value=15001, step=1)
            update_trade_type = st.selectbox("Updated Trade Type", ["BUY", "SELL"], key="update_type")
            update_quantity = st.number_input("Updated Quantity", min_value=0.0, value=25.0, step=1.0)


        with u2:
            update_price = st.number_input("Updated Price", min_value=0.0, value=150.00, step=0.01)
            update_trade_asset = st.number_input("Updated Asset ID", min_value=1, value=13001, step=1)


        update_submit = st.form_submit_button("Update Trade")

        if update_submit:
            payload = {
                "trade_type": update_trade_type,
                "quantity": float(update_quantity),
                "price": float(update_price),
                "trade_asset": int(update_trade_asset)
            }

            try:
                update_res = requests.put(f"http://web-api:4000/trades/{update_trade_id}", 
                                          json=payload)
                update_data = update_res.json()

                if update_res.status_code == 200:
                    st.success("Trade updated successfully.")
                else:
                    st.error(f"Failed to update trade: {update_data}")

            except Exception as e:
                logger.error(f"Error updating trade: {e}")
                st.error("Failed to update trade.")

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
