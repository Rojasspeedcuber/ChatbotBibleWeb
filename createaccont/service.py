import streamlit as st
from api.service import Auth


def login(email, username, password):
    auth_service = Auth()
    response = auth_service.get_token(
        email=email,
        username=username,
        password=password
    )
    if response.get('error'):
        st.error(f'Falha ao realizar criação de conta: {response.get('error')}')
    else:
        st.session_state.token = response.get('access')
        st.rerun()
