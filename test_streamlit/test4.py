import streamlit as st
import random

st.title("Demo sin session_state")
#Test without state_session
# Lista de opciones
opciones = ["Dataset A", "Dataset B", "Dataset C"]

seleccionados = []

# Checkboxes
for op in opciones:
    if st.checkbox(op):
        seleccionados.append(op)

st.write("Selección actual:", seleccionados)

# Botón para procesar
if st.button("Procesar selección"):
    resultados = []
    st.write("Resultados:", seleccionados)
    for item in seleccionados:
        datos = [random.randint(0, 10) for _ in range(5)]
        resultados.append((item, datos))

    st.write("Resultados:", resultados,seleccionados)