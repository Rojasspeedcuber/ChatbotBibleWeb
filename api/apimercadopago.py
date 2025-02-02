import streamlit as st
import requests
import sqlite3
import os
from decouple import config
from payments.page import verificar_pagamento

# Configuração das credenciais do Mercado Pago
os.environ['CLIENT_ID'] = config('CLIENT_ID')
os.environ['CLIENT_SECRET'] = config('CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8501"

AUTH_URL = "https://auth.mercadopago.com/authorization"
TOKEN_URL = "https://api.mercadopago.com/oauth/token"

DATABASE_PATH = "databases/usuarios.sqlite"


def login_oauth():
    """Redireciona o usuário para o login do Mercado Pago."""
    url = f"{AUTH_URL}?response_type=code&client_id={'CLIENT_ID'}&redirect_uri={REDIRECT_URI}"
    st.markdown(f"[🔑 Login com Mercado Pago]({url})", unsafe_allow_html=True)


def check_oauth_callback():
    """Verifica se há um código de autorização e troca por um token de acesso."""
    params = st.query_params()

    if "code" in params:
        auth_code = params["code"][0]
        access_token = get_access_token(auth_code)

        if access_token:
            usuario = get_user_info(access_token)
            if usuario:
                # Verifica pagamento antes de liberar acesso
                verificar_pagamento(usuario)
                return usuario
    else:
        st.error("Erro ao autenticar com Mercado Pago.")

    return None


def get_access_token(auth_code):
    """Troca o código de autorização por um access token."""
    payload = {
        "client_id": 'CLIENT_ID',
        "client_secret": 'CLIENT_SECRET',
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")

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
