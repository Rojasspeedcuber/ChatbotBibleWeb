import streamlit as st
from createaccont.service import login
from api.apimercadopago import gerar_link_pagamento


def create_account():
    st.title('Criar conta')

    username = st.text_input('Usuário')
    email = st.text_input('Email')
    password = st.text_input(label='Senha', type='password')

    link = gerar_link_pagamento()

    # Adiciona um print para depuração
    print("Link de pagamento gerado:", link)

    if isinstance(link, str) and link.startswith("http"):
        if st.link_button(label='Criar conta', url=link):
            login(username=username, email=email, password=password)
    else:
        st.error("Erro ao gerar link de pagamento. Tente novamente.")
