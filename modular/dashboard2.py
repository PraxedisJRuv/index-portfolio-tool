import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Inputs import tickers
import random 

st.set_page_config(layout="wide")

st.title("Portfolio Analytics Dashboard")

if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

if "resultados" not in st.session_state:
    st.session_state.resultados = []

if "graficas" not in st.session_state:
    st.session_state.graficas = []

st.subheader("Selecciona stock")

for op in tickers:
    checked = st.multiselect(op, key=op)

    if checked:
        if op not in st.session_state.seleccionados:
            st.session_state.seleccionados.append(op)
    else:
        if op in st.session_state.seleccionados:
            st.session_state.seleccionados.remove(op)


if st.button("Procesar selección"):

    resultados = []

    for item in st.session_state.seleccionados:
        datos = [random.randint(0, 10) for _ in range(10)]
        resultados.append((item, datos))

    st.session_state.resultados = resultados
