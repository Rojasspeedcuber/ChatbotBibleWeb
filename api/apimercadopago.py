import streamlit as st
import requests
import sqlite3
from decouple import config
from payments.page import verificar_pagamento

# Configuração das credenciais do Mercado Pago
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
REDIRECT_URI = "https://chatbotgenesisweb.streamlit.app/"

AUTH_URL = "https://auth.mercadopago.com/authorization"
TOKEN_URL = "https://api.mercadopago.com/oauth/token"

DATABASE_PATH = "databases/usuarios.sqlite"


def get_access_token(auth_code):
    """Troca o código de autorização por um access token."""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=payload)

    if response.status_code == 200:
        return response.json().get('access_token')

    st.error("Erro ao obter access token.")
    return None


def get_user_info(access_token):
    """Obtém as informações do usuário autenticado via Mercado Pago."""
    url = "https://api.mercadopago.com/users/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        usuario = user_data.get("email")

        if usuario:
            salvar_usuario(usuario)
            return usuario

    st.error("Erro ao obter informações do usuário.")
    return None


def salvar_usuario(usuario):
    """Salva o usuário no banco de dados se ainda não existir."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    """)
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (username) VALUES (?)", (usuario,))
    conn.commit()
    conn.close()
