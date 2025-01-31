import streamlit as st
from createaccont.service import login
from api.apimercadopago import gerar_link_pagamento


def create_account():

    st.title('Criar conta')

    username = st.text_input('Usuário')
    email = st.text_input('Email')
    password = st.text_input(
        label='Senha',
        type='password'
    )

    if st.link_button(label='Criar conta', url=gerar_link_pagamento()):
        login(
            username=username,
            email=email,
            password=password
        )
