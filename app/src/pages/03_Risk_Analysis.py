import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Risk Analysis")

st.write(f"### Hi, {st.session_state['first_name']}.")

st.write("Review Sharpe ratio, volatility, and drawdown across strategies.")

#loading of all risk metrics

try:
    all_risk_res= requests.get("http://web-api:4000/riskmetrics")
    all_risk_data=all_risk_res.json()
    if all_risk_res.status_code != 200:
        st.error(f"Could not load risk metrics: {all_risk_data}")
        st.stop()
    all_risk_df = pd.DataFrame(all_risk_data)
except Exception as e:
    logger.error(f"error loading all risk metrics. {e}")
    st.error("failed to load risk metrics overview.")
    st.stop()

#top overview table
st.subheader("All Strategy Risk Metrics")
if len(all_risk_df) >0:
    display_df = all_risk_df.copy()
    for col in ["sharpe_ratio","volatility","drawdown"]:
        if col in display_df.columns:
            display_df[col] = pd.to_numeric(display_df[col], errors="coerce").round(2)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("No risk metric records found.")
    st.stop()
st.divider()

#strategy selector
strategy_options={
    "16001 - Tech Momentum": 16001,
    "16002 - Mean Reversion": 16002,
    "16003 - AI Growth Rotation": 16003,
    "16004 - Legacy ETF Hedge": 16004,
}

selected_strategy = st.selectbox(
    "Select Strategy",
    list(strategy_options.keys()),
    index=0
)

strategy_id = strategy_options[selected_strategy]


try: 
    risk_res = requests.get(f"http://web-api:4000/riskmetrics/{strategy_id}")
    risk_data = risk_res.json()
    if risk_res.status_code!=200:
        st.error(f"Could not load selected strategy risk metrics: {risk_data}")
        st.stop()
    risk_df = pd.DataFrame(risk_data)
except Exception as e:
    logger.error(f"error loading selected risk metrics: {e}")
    st.error("failed to load detailed risk analysis.")
    st.stop()

st.subheader("Detailed Risk Overview")

if len(risk_df)>0:
    latest = risk_df.iloc[0]
    sharpe = round(float(latest["sharpe_ratio"]),2)
    volatility = round(float(latest["volatility"]),2)
    drawdown= round(float(latest['drawdown']),2)
    col1,col2,col3=st.columns(3)
    col1.metric("Sharpe Ratio:",f"{sharpe:.2f}")
    col2.metric("Volatility:",f"{volatility:.2f}")
    col3.metric("Drawdown:",f"{drawdown:.2f}")

    st.divider()

    st.subheader("Risk Interpretation")
    info1,info2, info3 = st.columns(3)
    with info1:
        st.markdown("**Sharpe Ratio**")
        if sharpe >= 1.0:
            st.success("Strong risk-adjusted performance")
        else:
            st.warning("Lower risk-adjusted performance")
    with info2:
        st.markdown("**Volatility**")
        if volatility <= 0.15:
            st.success("Relatively stable returns")
        else:
            st.warning("Higher return variability")
    with info3:
        st.markdown("**Drawdown**")
        if sharpe <=0.10:
            st.success("Limited downside exposure.")
        else:
            st.warning("Larger peak to trough decline")
    st.divider()


    st.subheader("Detailed Risk Records")

    risk_display_df = risk_df.copy()
    for col in ["sharpe_ratio","volatility","drawdown"]:
        if col in risk_display_df.columns:
            risk_display_df[col] = pd.to_numeric(risk_display_df[col], errors="coerce").round(2)
    st.dataframe(risk_display_df, use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Risk Metric Comparison")
    chart_df=pd.DataFrame({
        "Metric": ['Sharpe Ratio', 'Volatility', 'Drawdown'],
        'Value': [sharpe, volatility, drawdown]
    })
    st.bar_chart(chart_df.set_index('Metric'), use_container_width=True)
else:
    st.info("No detailed risk records found for this strategy.")
