import streamlit as st
from process import procesado

opciones=["A","B","C"]
st.header("test_1")
options=st.multiselect("Select the Stocks:",opciones)
st.write("you selected", len(options),"opciones",type(options))
st.write(options)

st.button("accionado")
if st.button("accionar"):
    st.text("seleccionado")

seleccionados = []

for op in opciones:
    if st.checkbox(op, key=op):
        seleccionados.append(op)

st.write("Seleccionados:", seleccionados)


opciones=[1,2,3]
options2=st.multiselect("Select the Stocks:",opciones)
st.write("you selected", len(options2),"opciones",)
st.write(procesado(options2),type(options2))

