import sqlite3
import hashlib

DATABASE_PATH = "databases/login.sqlite"


def criar_db():
    """Cria o banco de dados se ainda não existir."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            senha TEXT
        )
    """)
    conn.commit()
    conn.close()


def hash_senha(senha):
    """Retorna o hash SHA-256 da senha."""
    return hashlib.sha256(senha.encode()).hexdigest()


def cadastrar_usuario(username, senha):
    """Cadastra um novo usuário."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))
    conn.commit()
    conn.close()


def verificar_login(username, senha):
    """Verifica se o login é válido."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT senha FROM usuarios WHERE username = ?", (username))
    user = cursor.fetchone()
    conn.close()
    return user is not None and user[0] == hash_senha(senha)
