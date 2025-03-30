from database import Database
from auth import Auth
import hashlib

# Função para adicionar usuários manualmente
def criar_usuarios_iniciais():
    db = Database()
    db.insert_usuario("Admin", "admin@admin.com", "123", tipo="admin")
    db.insert_usuario("teste", "teste@cliente.com", "123", tipo="comum")
    db.close()

criar_usuarios_iniciais()
