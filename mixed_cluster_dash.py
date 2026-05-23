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
import modular.dashboard_utilsmix as du
from modular.Inputs import stocks, indexes, types_period

st.set_page_config(layout="wide")
st.title("Portfolio Analytics Dashboard")

#  inputs
tickers = [ "Bimbo",
    "Cemex",
    "Alfa SA A",
    "Alsea SA",
    "America Movil SAB de CV B",
    "Arca Continental SAB de CV",
    "Banco del Bajio SA",
    "Becle SA De CV",
    "Bolsa Mexicana de Valores SA de CV" ,
    "Coca Cola Femsa SAB de CV UBL",
    "Corporacion Inmobiliaria Vesta SAB de CV",
    "El Puerto de Liverpool SAB de CV",
    "Fomento Economico Mexicano SAB de CV",
    "Genomma Lab Internacional SA de CV",
    "Gentera SAB de CV",
    "Gruma SAB B",
    "Grupo Aeroportuario del Centro Norte SAB de CV",
    "Grupo Aeroportuario del Sureste SAB de CV B",
    "Grupo Carso SAB de CV",
    "Grupo Cementos de Chihuahua SAB de CV",
    "Grupo Comercial Chedraui SA de CV",
    "Grupo Financiero Banorte O",
    "Grupo Financiero Inbursa O",
    "Grupo Mexico SAB de CV B",
    "Grupo Televisa SAB CPO",
    "Industrias Peñoles",
    "Kimberly Clark de Mexico SAB de CV A",
    "La Comer SAB de CV UBC",
    "Megacable Holdings SAB de CV",
    "Orbia Advance Corporation SAB de CV",
    "Qualitas Controladora SAB de CV",
    "Regional SA de CV",
    "Walmart de Mexico SAB de CV"]
index_name = st.selectbox("Índice", indexes)

col1, col2 = st.columns(2)
start = col1.date_input("Start", datetime(2019,4,11))
end = col2.date_input("End", datetime(2024,12,31))

period = st.selectbox("Period", types_period, index=1)
period = pd.Timedelta(period)

num_medoids = st.number_input("Clusters", 1, 10, 2)

lambda_for_Markowitz = st.number_input("Lambda for Markowitz", 0.0, 1.0, 0.5)

# Buttons for process
st.header("Analyze")
if st.button("Ejecutar Proceso 1"):
    du.run_process_1(tickers,index_name,period,start,end)

st.header("Clustering por correlaciones")
if st.button("Ejecutar Proceso 2"):
    if "p1" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_2(tickers,num_medoids,period)

st.header("Clustering por desviaciones")
if st.button("Ejecutar Proceso 3"):
    if "p2" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_3(tickers,num_medoids,period)

st.header("Clustering combinado")
if st.button("Ejecutar Proceso 4"):
    if "p3" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_4(tickers,num_medoids,period)


st.header("Markowitz Optimization")
if st.button("Ejecutar Proceso 5"):
    if "p4" not in st.session_state:
        st.warning("Primero ejecuta el Proceso 1")
    else:
        du.run_process_5(tickers,period,lambda_for_Markowitz)


# graphs
st.divider()

if "p1" in st.session_state:
    st.subheader("Portfolio vs Index")
    p1 = st.session_state["p1"]
    du.metrics_and_chart(p1["returns"], p1["index_returns"], start, end, p1["num_periods"],key="chart_p1")

if "p2" in st.session_state:
    st.subheader("Clusterized portfolio by correlations vs Index")
    p2 = st.session_state["p2"]
    du.metrics_and_chart(p2["returns"], p2["index_returns"], start, end, p2["num_periods"],key="chart_p2")

if "p3" in st.session_state:
    st.subheader("Clusterized portfolio by deviations vs Index")
    p3 = st.session_state["p3"]
    du.metrics_and_chart(p3["returns"], p3["index_returns"], start, end, p3["num_periods"],key="chart_p3")

if "p4" in st.session_state:
    st.subheader("Mixed clusterized portfolio vs Index")
    p4 = st.session_state["p4"]
    du.metrics_and_chart(p4["returns"], p4["index_returns"], start, end, p4["num_periods"],key="chart_p4")

if "p5" in st.session_state:
    st.subheader("Optimized portfolio vs Index")
    p5 = st.session_state["p3"]
    du.metrics_and_chart(p5["returns"], p5["index_returns"], start, end, p5["num_periods"],key="chart_p5")