import streamlit as st
import matplotlib.pyplot as plt
import random

st.title("Demo con guardados")

# Inicializar estado
if "seleccionados" not in st.session_state:
    st.session_state.seleccionados = []

if "resultados" not in st.session_state:
    st.session_state.resultados = []

if "graficas" not in st.session_state:
    st.session_state.graficas = []

# Lista de opciones
st.subheader("Selecciona opciones")

opciones = ["Dataset A", "Dataset B", "Dataset C"]

for op in opciones:
    checked = st.checkbox(op, key=op)

    if checked:
        if op not in st.session_state.seleccionados:
            st.session_state.seleccionados.append(op)
    else:
        if op in st.session_state.seleccionados:
            st.session_state.seleccionados.remove(op)

st.write("Seleccion actual:", st.session_state.seleccionados)

# Procesar datos
if st.button("Procesar selección"):
    resultados = []

    for item in st.session_state.seleccionados:
        # Simulación de procesamiento
        datos = [random.randint(0, 10) for _ in range(10)]
        resultados.append((item, datos))

    st.session_state.resultados = resultados

# Mostrar resultados
if st.session_state.resultados:
    st.subheader("Resultados generados")

    for nombre, datos in st.session_state.resultados:
        st.write(f"{nombre}: {datos}")

# Crear gráfica nueva
if st.button("Agregar gráfica"):
    if st.session_state.resultados:
        fig, ax = plt.subplots()

        for nombre, datos in st.session_state.resultados:
            ax.plot(datos, label=nombre)

        ax.legend()
        ax.set_title("Gráfica generada")

        # Guardar gráfica
        st.session_state.graficas.append(fig)

# Mostrar todas las gráficas acumuladas
if st.session_state.graficas:
    st.subheader("Gráficas acumuladas")

    for i, fig in enumerate(st.session_state.graficas):
        st.pyplot(fig)

# Botón para limpiar todo
if st.button("Resetear app"):
    st.session_state.seleccionados = []
    st.session_state.resultados = []
    st.session_state.graficas = []
    st.rerun()

