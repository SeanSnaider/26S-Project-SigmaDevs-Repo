import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

JANE_PORTFOLIO = 102

hour = datetime.now().hour
if hour < 12:
    greeting = "Morning"
elif hour < 17:
    greeting = "Afternoon"
else:
    greeting = "Evening"

portfolio_value = 245800
try:
    port_res = requests.get(f"http://web-api:4000/portfolios/{JANE_PORTFOLIO}")
    if port_res.status_code == 200:
        port_data = port_res.json()
        portfolio_value = float(port_data.get('total_value', 245800))
except Exception as e:
    logger.error(f"Error fetching portfolio: {e}")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.title(f"{greeting}, {st.session_state['first_name']}.")
    st.markdown("Your portfolio is up by :green[**1.5%**] today")
    st.metric("Balance", f"${portfolio_value:,.0f}")

    period = st.radio(
        "",
        ["1y", "YTD", "1m", "1w", "1d"],
        horizontal=True,
        label_visibility="collapsed"
    )

    period_days = {
        "1y":  365,
        "YTD": (datetime.now() - datetime(datetime.now().year, 1, 1)).days,
        "1m":  30,
        "1w":  7,
        "1d":  24,
    }
    seeds = {"1y": 1, "YTD": 2, "1m": 3, "1w": 4, "1d": 5}
    n = period_days[period]

    np.random.seed(seeds[period])
    prices = np.cumsum(np.random.randn(n) * (portfolio_value * 0.003)) + portfolio_value * 0.85

    if period == "1d":
        idx = [datetime.now() - timedelta(hours=n - i) for i in range(n)]
    else:
        idx = [datetime.now() - timedelta(days=n - i) for i in range(n)]

    st.line_chart(pd.DataFrame({"Portfolio Value ($)": prices}, index=idx))

with col_right:
    st.title("Industry Standards")
    st.divider()

    standards = [
        ("Your Portfolio", "+32%", "green"),
        ("S&P 500",        "+12%", "green"),
        ("Oil Barrel",     "-5%",  "red"),
        ("Gold",           "+15%", "green"),
        ("Silver",         "+69%", "green"),
        ("Inflation",      "+29%", "red"),
    ]

    for name, val, color in standards:
        c1, c2 = st.columns([2, 1])
        c1.markdown(f"**{name}**")
        c2.markdown(f":{color}[**{val}**]")
        st.divider()
