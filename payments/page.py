import streamlit as st
from payments.service import criar_assinatura


def exibir_interface_pagamento():
    st.header("Assinatura não realizada ou expirada! Renove para continuar.")
    st.write(
        "Para continuar usando o Chatbot Gênesis, assine por apenas R$30,00 por 4 meses.")

    st.text_input("Email")
    if st.button("Continuar"):
        # Gera o link para a assinatura
        link_pagamento = criar_assinatura()
        if link_pagamento:
            st.markdown(
                f"[Clique aqui para realizar ou renovar sua assinatura]({link_pagamento})")
        else:
            st.error(
                "Erro ao gerar o link de assinatura. Tente novamente mais tarde.")
