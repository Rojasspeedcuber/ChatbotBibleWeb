import streamlit as st
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

    # Verifica se o usuário existe e se a senha informada bate com o hash armazenado
    return user is not None and user[1] == hash_senha(senha)
