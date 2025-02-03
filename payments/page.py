import streamlit as st
from payments.service import criar_pagamento_checkout_pro


import streamlit as st


def exibir_link_pagamento():
    pagamento_url = criar_pagamento_checkout_pro()

    if pagamento_url:
        st.markdown(f"[Clique aqui para pagar]({pagamento_url})")
    else:
        st.error("Erro ao gerar pagamento.")
