import streamlit as st
from payments.service import criar_pagamento_checkout_pro
from decouple import config


import streamlit as st


def exibir_link_pagamento():
    pagamento_url = criar_pagamento_checkout_pro()

    st.markdown(f"[Clique aqui para pagar]({pagamento_url})")
