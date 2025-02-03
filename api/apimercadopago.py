import mercadopago
import streamlit as st
import requests
from decouple import config

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
REDIRECT_URI = "https://chatbotgenesisweb.streamlit.app/"

AUTH_URL = "https://auth.mercadopago.com/authorization"
TOKEN_URL = "https://api.mercadopago.com/oauth/token"


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
