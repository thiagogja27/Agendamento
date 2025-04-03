import streamlit as st

# essa tela sera onde o cliente pode se comunicar com o terminal (acho que seria bom se o motorista pudesse entrar em contato também. o assunto poderia ser algo relacionado ao ID do cadastro e quem está chamando [motorista, ou transportadora])

class Suporte:
    def show(self):
        st.title("Suporte")
        st.write("Entre em contato com o suporte para obter ajuda.")
