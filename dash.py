import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import modular.benchmarks as bm
import modular.portfolio as port
from modular.optimization.Clustering.medoids.kmedoids import clustering_medoids
from modular.optimization.Markowitz.usual.markowitz import markowitz_of_periods
from modular.extraction import full_dataframe_extraction, index_dataframe_extraction
import modular.dashboard_utils as du
from modular.inputs import stocks, indexes, types_period

st.set_page_config(layout="wide")
st.title("Portfolio Analytics Dashboard")

#  inputs
tickers = st.multiselect("Select stock tickers",stocks)

index_name = st.selectbox("Índice", indexes)

col1, col2 = st.columns(2)
start = col1.date_input("Start", datetime(2024,3,17))
end = col2.date_input("End", datetime(2026,3,15))

period = st.selectbox("Period", types_period, index=1)
period = pd.Timedelta(period)

num_medoids = st.number_input("Clusters", 1, 10, 2)

lambda_for_Markowitz = st.number_input("Lambda for Markowitz", 0.0, 1.0, 0.5)

# Buttons for process
st.header("Analyze")
if st.button("Ejecutar Proceso 1"):
    du.run_process_1(tickers,index_name,period,start,end)

st.header("Clustering")
if st.button("Ejecutar Proceso 2"):
    if "p1" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_2(tickers,num_medoids,period)

st.header("Markowitz Optimization")
if st.button("Ejecutar Proceso 3"):
    if "p1" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_3(tickers,period,lambda_for_Markowitz)


# graphs
st.divider()

if "p1" in st.session_state:
    st.subheader("Portfolio vs Index")
    p1 = st.session_state["p1"]
    du.metrics_and_chart(p1["returns"], p1["index_returns"], start, end, p1["num_periods"],key="chart_p1")

if "p2" in st.session_state:
    st.subheader("Clusterized portfolio vs Index")
    p2 = st.session_state["p2"]
    du.metrics_and_chart(p2["returns"], p2["index_returns"], start, end, p2["num_periods"],key="chart_p2")

if "p3" in st.session_state:
    st.subheader("Optimized portfolio vs Index")
    p3 = st.session_state["p3"]
    du.metrics_and_chart(p3["returns"], p3["index_returns"], start, end, p3["num_periods"],key="chart_p3")