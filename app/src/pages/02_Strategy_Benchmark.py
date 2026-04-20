import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Strategy vs Benchmark")

st.write(f"### Hi, {st.session_state['first_name']}.")

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




strategy_res = requests.get(f"http://web-api:4000/strategies/{strategy_id}")
performance_res = requests.get(f"http://web-api:4000/strategies/{strategy_id}/performance")
benchmark_res = requests.get(f"http://web-api:4000/strategies/{strategy_id}/benchmark")

strategy = strategy_res.json()
performance = performance_res.json()
benchmark = benchmark_res.json()
if strategy_res.status_code !=200:
    st.error(f"Could not load strategy data: {strategy}")
    st.stop()
if not isinstance(strategy, dict):
    st.error("Strategy response is not in the expected format.")
    st.write(strategy)
    st.stop()

st.subheader("Strategy Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Strategy:", strategy["strategy_name"])
col2.metric("Type:", strategy['strategy_type'])
col3.metric('Status:', strategy['status'])

st.divider()

st.subheader("Performance")
perf_df =pd.DataFrame(performance)

if performance_res.status_code==200 and len(perf_df) >0:
    latest_perf = perf_df.iloc[0]
    col1,col2,col3 = st.columns(3)
    col1.metric("Portfolio Value:", f"${latest_perf['port_value']:,.2f}")
    col2.metric(
        "Daily P&L:",
        f"${latest_perf['daily_PNL']:,.2f}",
        delta=f"{latest_perf['daily_PNL']:,.2f}"
    )
    col3.metric(
        "Cumulative P&L:",
        f"${latest_perf['cumulative_PNL']:,.2f}",
        delta=f"{latest_perf['cumulative_PNL']:,.2f}"
    )
    st.write("### Performance Table")
    st.dataframe(perf_df, use_container_width=True, hide_index=True)
else:
    st.info("No performance data found.")
st.divider()

st.subheader("Benchmark Overview")
bench_df = pd.DataFrame(benchmark)

if benchmark_res.status_code==200 and len(bench_df)>0:
    latest_bench = bench_df.iloc[0]
    col1,col2,col3=st.columns(3)
    col1.markdown("Benchmark:")
    col1.markdown(f"{latest_bench.get('benchmark_name')}")
    col2.metric("Ticker:", latest_bench.get("ticker"))
    col3.metric("Value:",
                f"${latest_bench.get('current_value')}"
                )
    st.write("### Benchmark Table")
    st.dataframe(bench_df, use_container_width=True, hide_index = True)
else:
    st.info("No benchmark data found.")
st.divider()


st.subheader("Comparison Summary")
compare_df = pd.DataFrame({
    "Measure": [
    "Strategy Name",
    "Strategy Type",
    "Strategy Status",
    "Portfolio Value",
    "Daily P&L",
    "Cumulative P&L",
    "Benchmark Name",
    "Benchmark Ticker",
    "Benchmark value"
    ],
    "Value":[
        strategy["strategy_name"],
        strategy["strategy_type"],
        strategy["status"],
        f"${latest_perf['port_value']:,.2f}",
        f"${latest_perf['daily_PNL']:,.2f}",
        f"${latest_perf['cumulative_PNL']:,.2f}",
        latest_bench["benchmark_name"],
        latest_bench["ticker"],
        f"${float(latest_bench['current_value']):,.2f}"
    ]
})

st.dataframe(compare_df, use_container_width=True,hide_index=True)

st.divider()

#Strategy Controls
st.subheader("Update Strategy")

left_col, right_col = st.columns(2)
with left_col:
    new_parameter = st.text_input(
        "Update Parameter",
        value = strategy["parameter"]
    )
    if st.button("Save Parameter", use_container_width=True):
        payload = {"parameter": new_parameter}
        update_res=requests.put(
            f"http://web-api:4000/strategies/{strategy_id}",
            json=payload
        )
        if update_res.status_code == 200:
            st.success("Strategy parameter updated successfully.")
        else: 
            st.error("Failed to update parameter.")
with right_col:
    current_status = strategy.get("status",'active')
    if current_status == "active" or current_status == "Active":
        status_index=0
    else: 
        status_index=1
    new_status = st.selectbox(
        "Update Status",
        ["active","inactive"],
        index=status_index
    )
    if st.button("Save Status", use_container_width=True):
        payload = {"status": new_status}
        update_res=requests.put(
            f"http://web-api:4000/strategies/{strategy_id}",
            json=payload
        )
        if update_res.status_code ==200:
            st.success("Strategy status updated successfully.")
        else: 
            st.error("Failed to update status.")
st.divider()

#Create new strategy

st.subheader("Create New Strategy")
with st.form("create_strategy_form"):
    create_col1, create_col2 = st.columns(2)
    with create_col1:
        strategy_name = st.text_input("Strategy Name")
        strategy_type = st.text_input("Strategy Type")
        parameter = st.text_input("Parameter")
        status = st.selectbox("Status", ["active","inactive"])
    with create_col2:
        new_strategy_id = st.number_input("Strategy ID", min_value=1, value=20001, step=1)
        trade_strat = st.number_input("Trade ID", min_value=1, value = 15001, step=1)
        port_strat= st.number_input("Portfolio ID", min_value=1, value = 101,step=1)
    create_submitted = st.form_submit_button("Create Strategy")
    if create_submitted:
        payload = {
            "strategy_name": strategy_name,
            "strategy_type": strategy_type,
            "parameter": parameter,
            "status": status,
            "strategy_id": int(new_strategy_id),
            "trade_strat": int(trade_strat),
            "port_strat": int(port_strat)
        }
        create_res = requests.post(
            "http://web-api:4000/strategies",
            json=payload
        )
        if create_res.status_code==200 or create_res.status_code==201:
            st.success("New Strategy created successfully.")
        else: 
            st.error("failed to create strategy.")
            st.write("Please fill out every field.")
