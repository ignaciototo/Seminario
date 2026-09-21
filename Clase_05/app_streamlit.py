import streamlit as st

st.title("Clase 05 - Streamlit")

nombre = st.text_input("Ingresá tu nombre:")
if st.button("Enviar"):
  if nombre:
    st.success(f"¡Hola {nombre}! App corriendo en Streamlit Community Cloud.")
  else:
    st.warning("Escribí un nombre primero.")