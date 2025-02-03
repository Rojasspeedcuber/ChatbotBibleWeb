import streamlit as st
from payments.service import criar_pagamento_checkout_pro
from decouple import config

CLIENT_ID = config('CLIENT_ID')


def verificar_pagamento():
    """Direciona o usuário para realizar o pagamento."""
    st.warning("Pagamento necessário para acessar o app.")

    if st.button("Realizar Pagamento"):
        pagamento_url = criar_pagamento_checkout_pro(CLIENT_ID)
        st.page_link(f"[Clique aqui para pagar]({pagamento_url})")

    st.stop()  # Para a execução do Streamlit até que o usuário pague
