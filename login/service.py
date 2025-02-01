import streamlit as st
from api.service import Auth
from decouple import config
import os

os.environ["ACCESS_TOKEN"] = config("ACCESS_TOKEN")


def login(username, password):
    auth_service = Auth("ACCESS_TOKEN")
    response = auth_service.get_token(
        username=username,
        password=password
    )
    if response.get('error'):
        st.error(f'Falha ao realizar login: {response.get('error')}')
    else:
        st.session_state.token = response.get('access')
        st.rerun()
