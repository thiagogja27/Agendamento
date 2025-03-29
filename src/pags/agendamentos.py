import streamlit as st
import sqlite3
from database import Database
import time

class Agendamentos:
    def __init__(self):
        self.db = Database()

    def show(self):
        st.title("Agendamentos")

        user_id = st.session_state["auth_user"]["id"]
        user_tipo = st.session_state["auth_user"]["tipo"]

        if user_tipo == "admin":
            query = "SELECT id, usuario_id, titulo, descricao, data FROM agendamentos"
            params = ()
        else:
            query = "SELECT id, titulo, descricao, data FROM agendamentos WHERE usuario_id = ?"
            params = (user_id,)

        # Criar novo agendamento
        with st.form("Novo Agendamento"):
            titulo = st.text_input("Título")
            cliente = st.text_input("Cliente")
            terminal = st.selectbox("Escolha o Terminal", ["Terminal 1", "Terminal 2"])
            tipo_cms = st.selectbox("Escolha o tipo do caminhão", ["Tipo 1", "Tipo 2"])
            descricao = st.text_area("Descrição")
            data = st.date_input("Data")

            if st.form_submit_button("Salvar"):
                if user_tipo == "admin":
                    titulo = "ADMIN_" + str(user_id) + " " + titulo
                    self.db.cursor.execute(
                        "INSERT INTO agendamentos (usuario_id, titulo, descricao, data, data_cadastro) VALUES (?, ?, ?, ?, ?)",
                        (user_id, titulo, descricao, data, time.time()),
                    )
                else:
                    self.db.cursor.execute(
                        "INSERT INTO agendamentos (usuario_id, titulo, descricao, data, data_cadastro) VALUES (?, ?, ?, ?, ?)",
                        (user_id, titulo, descricao, data, time.time()),
                    )
                self.db.conn.commit()
                st.success("Agendamento criado com sucesso!")
                # st.rerun()

        self.db.cursor.execute(query, params)
        agendamentos = self.db.cursor.fetchall()

        if agendamentos:
            for ag in agendamentos:
                st.write(f"**Título:** {ag[1]}")
                st.write(f"**Descrição:** {ag[2]}")
                st.write(f"**Data:** {ag[3]}")
                st.write("---")
        else:
            st.write("Nenhum agendamento encontrado.")