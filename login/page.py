import streamlit as st
from login.service import verificar_login, cadastrar_usuario
from api.apimercadopago import login_oauth, check_oauth_callback
from payments.page import verificar_pagamento


def login_screen(selecao_usuario):
    """Tela de login com autenticação via senha ou Mercado Pago."""
    st.title("Login no Aplicativo")

    menu = selecao_usuario

    if menu == "Login":
        st.subheader("Faça login")
        username = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if verificar_login(username, senha):
                st.success(f"Bem-vindo, {username}!")
                verificar_pagamento(username)
                return username
            else:
                st.error("Usuário ou senha incorretos!")

    elif menu == "Login com Mercado Pago":
        st.subheader("Autenticação via Mercado Pago")

        if "code" in st.st.query_params():
            usuario = check_oauth_callback()
            if usuario:
                st.success(f"Bem-vindo, {usuario}!")
        else:
            login_oauth()

    elif menu == "Cadastrar":
        st.subheader("Crie uma conta")
        new_username = st.text_input("Novo usuário")
        new_senha = st.text_input("Nova senha", type="password")

        if st.button("Cadastrar"):
            if new_username and new_senha:
                cadastrar_usuario(new_username, new_senha)
                st.success("Usuário cadastrado com sucesso! Agora faça login.")
            else:
                st.warning("Preencha todos os campos!")

    return None
