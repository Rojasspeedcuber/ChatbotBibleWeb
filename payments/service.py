import mercadopago
import requests
import streamlit as st
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')


def criar_pagamento_checkout_pro():
    """Cria uma preferência de pagamento no Mercado Pago com Checkout Pro usando um token fixo."""

    url = "https://api.mercadopago.com/checkout/preferences"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "items": [
            {
                "title": "Chatbot Gênesis",
                "quantity": 1,
                "unit_price": 60.00,
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
