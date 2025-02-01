import streamlit as st
from createaccont.service import login
from api.apimercadopago import gerar_link_pagamento


def create_account():
    st.title('Criar conta')

    username = st.text_input('Usuário')
    email = st.text_input('Email')
    password = st.text_input(label='Senha', type='password')

    link = gerar_link_pagamento()

    # Verificar se o link é uma string válida
    if isinstance(link, str) and link.startswith("http"):
        st.link_button(label="Criar conta", url=link)
    else:
        st.error("❌ Erro ao gerar link de pagamento.")
