import requests
# Importando a função para obter o access_token
from api.apimercadopago import get_access_token
import streamlit as st


def criar_pagamento_checkout_pro(auth_code):
    """Cria uma preferência de pagamento no Mercado Pago com Checkout Pro."""
    # Obtém o token de acesso usando o código de autorização
    access_token = get_access_token(auth_code)

    if not access_token:
        st.error("Não foi possível obter o token de acesso.")
        return None

    url = "https://api.mercadopago.com/checkout/preferences"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "items": [
            {
                "title": "Chatbot Gênesis",
                "quantity": 1,
                "unit_price": 45.00,
                "currency_id": "BRL"
            }
        ],
        "auto_return": "approved",  # Redireciona automaticamente após o pagamento ser aprovado
        "payment_methods": {
            "excluded_payment_types": [
                {"id": "ticket"}  # Excluir boletos, por exemplo
            ],
            # Número de parcelas (1 significa pagamento à vista)
            "installments": 1
        }
    }

    # Envia a requisição POST para criar a preferência de pagamento
    response = requests.post(url, json=payload, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 201:
        preference = response.json()
        # Retorna a URL do Checkout Pro para redirecionar o usuário
        return preference["init_point"]
    else:
        # Exibe os detalhes da resposta para depuração
        print(f"Erro ao criar pagamento: {response.status_code}")
        try:
            erro = response.json()  # Tenta capturar a resposta como JSON para analisar o erro
            print(f"Detalhes do erro: {erro}")
        except ValueError:
            print("Não foi possível decodificar a resposta como JSON.")
            print(f"Detalhes da resposta: {response.text}")
        return None
