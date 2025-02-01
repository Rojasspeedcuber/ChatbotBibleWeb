import streamlit as st
from createaccont.service import create_account
from api.apimercadopago import gerar_link_pagamento
import webbrowser


def show_create_account():
    st.title('Criar conta')

    username = st.text_input('Usuário')
    email = st.text_input('Email')
    password = st.text_input(label='Senha', type='password')

    link = gerar_link_pagamento()

    if st.link_button(label="Criar conta", url=link):
        create_account(
            username=username,
            email=email,
            password=password
        )
