import streamlit as st
import sqlite3
import hashlib
import bcrypt

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
    """Cadastra um novo usuário com a senha criptografada."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Gera o hash da senha antes de armazenar
    senha_hash = hash_senha(senha)

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha_hash))
        conn.commit()
        st.success("Usuário cadastrado com sucesso! Agora faça login.")
    except sqlite3.IntegrityError:
        st.error("Erro: Nome de usuário já existe!")
    finally:
        conn.close()


def verificar_login(username, senha):
    """Verifica se o login é válido."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Busca a senha criptografada do usuário no banco de dados
    cursor.execute(
        "SELECT senha FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()

    # Se o usuário não existir, retorna False
    if user is None:
        return False

    # Obtém o hash armazenado
    hash_armazenado = user[0]

    # Verifica a senha utilizando bcrypt
    return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))
