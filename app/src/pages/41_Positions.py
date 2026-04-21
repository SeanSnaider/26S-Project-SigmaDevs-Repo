import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Positions")
st.write(f"### Hi, {st.session_state['first_name']}.")

JANE_PORTFOLIO = 102

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("Portfolio")
    try:
        pos_res = requests.get(f"http://web-api:4000/StockPosition/{JANE_PORTFOLIO}")
        if pos_res.status_code != 200:
            st.error("Could not load positions.")
        else:
            positions = pos_res.json()
            rows = []
            for pos in positions:
                asset_res = requests.get(f"http://web-api:4000/asset/{pos['position_id']}")
                if asset_res.status_code == 200:
                    assets = asset_res.json()
                    asset = assets[0] if assets else {}
                else:
                    asset = {}

                qty = pos['qty_held']
                market_val = float(pos['market_value'])
                last_price = round(market_val / qty, 2) if qty else 0

                rows.append({
                    'Name': asset.get('asset_name', asset.get('ticker', '-')),
                    'Last Price': f"${last_price:,.2f}",
                    'All-time Loss/Gain': f"${float(pos['unrealized_PNL']):,.2f}",
                })

            if rows:
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No positions found.")
    except Exception as e:
        logger.error(f"Error loading positions: {e}")
        st.error("Failed to load positions.")

with col_right:
    st.subheader("Market Summary")

    m1, m2 = st.columns(2)
    m1.metric("S&P 500", "5,218", "+0.74%")
    m2.metric("NASDAQ", "16,340", "-0.21%")

    m3, m4 = st.columns(2)
    m3.metric("Oil (WTI)", "$82.14", "+1.05%")
    m4.metric("10Y Treasury", "4.42%", "-0.03%")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Standout Stocks**")
        st.markdown("NVDA &nbsp; +3.2%")
        st.markdown("AAPL &nbsp; -1.1%")
        st.markdown("TSLA &nbsp; +5.4%")
        st.markdown("META &nbsp; +2.7%")

    with c2:
        st.markdown("**Recent News**")
        st.markdown("- Fed holds rates steady")
        st.markdown("- Tech earnings beat")
        st.markdown("- Oil rises on supply cuts")
        st.markdown("- S&P hits new high")
