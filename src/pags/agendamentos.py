import streamlit as st
import sqlite3
from database import Database
import time
from datetime import date

class Agendamentos:
    def __init__(self):
        self.db = Database()
        self.hoje = date.today().isoformat()

    def show(self):
        st.title("Agendamentos")

        user_id = st.session_state["auth_user"]["id"]
        user_tipo = st.session_state["auth_user"]["tipo"]

        if user_tipo == "admin":
            query = "SELECT id, usuario_id, placa, descricao, data, cliente FROM agendamentos WHERE data = ?"
            params = (self.hoje,)
        else:
            query = "SELECT id, usuario_id, placa, descricao, data, cliente FROM agendamentos WHERE usuario_id = ? AND data = ?"
            params = (user_id, self.hoje)

        # Criar novo agendamento
        with st.form("Novo Agendamento"):
            placa = st.text_input("Placa Cavalo")
            cliente = st.selectbox("Escolha o Cliente", ["Cliente 1", "Cliente 2"])
            terminal = st.selectbox("Escolha o Terminal", ["Terminal 1", "Terminal 2"])
            nome_motorista = st.text_input("Nome do motorista")
            telefone_motorista = st.text_input("Telefone do motorista")
            documento_motorista = st.text_input("Documento do motorista")
            tipo_cms = st.selectbox("Escolha o tipo do caminhão", ["Tipo 1", "Tipo 2"])
            descricao = st.text_area("Descrição")
            data = st.date_input("Data")
            nf_xml = st.file_uploader("Por favor, selecione o XML da nota", type=["xml"], accept_multiple_files=True)

            if st.form_submit_button("Salvar"):
                if all([placa, cliente, terminal, nome_motorista, telefone_motorista, 
                    documento_motorista, tipo_cms, data, nf_xml]):
                    for xml_file in nf_xml:
                        xml_content = xml_file.read()
                        nome_arquivo = xml_file.name
                        if user_tipo == "admin":
                            placa = "ADMIN_" + str(user_id) + " " + placa
                            self.db.cursor.execute(
                                "INSERT INTO agendamentos (usuario_id, placa, descricao, data, data_cadastro, cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, nome_arquivo, nf_xml) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (user_id, placa, descricao, data, time.time(), cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, nome_arquivo, xml_content),
                            )
                        else:
                            self.db.cursor.execute(
                                "INSERT INTO agendamentos (usuario_id, placa, descricao, data, data_cadastro, cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, nome_arquivo, nf_xml) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (user_id, placa, descricao, data, time.time(), cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, nome_arquivo, xml_content),
                            )
                    self.db.conn.commit()
                    st.success("Agendamento criado com sucesso!")
                else:
                    st.error("Por favor, preencha todas as informações")

        self.db.cursor.execute(query, params)
        agendamentos = self.db.cursor.fetchall()

        col1, col2 = st.columns(2)

        agendamentos_cliente1 = [ag for ag in agendamentos if ag[5] == "Cliente 1"]
        agendamentos_cliente2 = [ag for ag in agendamentos if ag[5] == "Cliente 2"]

        with col1:
            st.subheader("Agendamentos Cliente 1")
            if agendamentos_cliente1:
                for ag in agendamentos_cliente1:
                    st.write(f"**Placa:** {ag[2]}")
                    st.write(f"**Descrição:** {ag[3]}")
                    st.write(f"**Data:** {ag[4]}")
                    st.write("---")
            else:
                st.write("Nenhum agendamento encontrado.")

        with col2:
            st.subheader("Agendamentos Cliente 2")
            if agendamentos_cliente2:
                for ag in agendamentos_cliente2:
                    st.write(f"**Placa:** {ag[2]}")
                    st.write(f"**Descrição:** {ag[3]}")
                    st.write(f"**Data:** {ag[4]}")
                    st.write("---")
            else:
                st.write("Nenhum agendamento encontrado.")