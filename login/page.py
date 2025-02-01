import streamlit as st
from login.service import login
from api.apimercadopago import gerar_link_pagamento
import webbrowser


def show_login():

    st.title('Login')

    username = st.text_input('Usuário')
    password = st.text_input(
        label='Senha',
        type='password'
    )

    if st.button('Login'):
        login(
            username=username,
            password=password
        )
        link = gerar_link_pagamento()
        webbrowser.open_new_tab(link)
