import sqlite3
import hashlib
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()

    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar_usuario(self, nome, email, senha, tipo="comum"):
        """Cadastra um novo usuário no sistema"""
        senha_hash = self.hash_senha(senha)
        try:
            self.db.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo),
            )
            self.db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, email, senha):
        """Realiza login e retorna as informações do usuário"""
        senha_hash = self.hash_senha(senha)
        self.db.cursor.execute(
            "SELECT id, nome, tipo FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha_hash),
        )
        user = self.db.cursor.fetchone()
        return user if user else None

# teste do teste testado