import streamlit as st
from payments.service import criar_pagamento, verificar_status_pagamento


def verificar_pagamento(usuario):
    """Verifica se o usuário tem pagamento aprovado, senão gera link."""
    if verificar_status_pagamento(usuario):
        st.success("Acesso liberado! Você já realizou o pagamento.")
        return True

    st.warning("Pagamento necessário para acessar o app.")

    if st.button("Realizar Pagamento"):
        pagamento_url = criar_pagamento(usuario)
        if pagamento_url:
            st.markdown(f"[Clique aqui para pagar]({pagamento_url})")
        else:
            st.error("Erro ao gerar pagamento.")

    st.stop()  # Para a execução do Streamlit até que o usuário pague
