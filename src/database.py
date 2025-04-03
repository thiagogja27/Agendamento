import sqlite3
import hashlib

# Criando o banco de dados, é util para manter o código organizado e sempre encontrar a tabela que precisamos. qlqr alteração aqui precisa ser revisada

DB_NAME = "agendamentos.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Cria as tabelas no banco de dados"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('comum', 'admin')) DEFAULT 'comum'
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                placa TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                cliente TEXT NOT NULL,
                terminal TEXT NOT NULL,
                tipo_cms TEXT NOT NULL,
                nome_motorista TEXT NOT NULL,
                telefone_motorista TEXT NOT NULL,
                documento_motorista TEXT NOT NULL,
                nome_arquivo TEXT NOT NULL,
                nf_xml TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        self.conn.commit()

    def insert_usuario(self, nome, email, senha, tipo="comum"):
        """Função para criar um usuário manualmente"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo),
            )
            self.conn.commit()
            print(f"Usuário {nome} criado com sucesso!")
        except sqlite3.IntegrityError:
            print(f"Erro: Email {email} já está em uso.")

    def close(self):
        self.conn.close()
