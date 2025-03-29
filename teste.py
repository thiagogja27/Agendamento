import streamlit as st

st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Escolha uma página:", ["Dashboard", "Agendamentos", "Suporte"])
st.write(f"Você selecionou a página: {pagina}")
