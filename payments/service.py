import requests
from decouple import config


def criar_pagamento():
    """Cria um link de pagamento no Mercado Pago."""
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {config('ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": "Chatbot Gênesis",
        "currency_id": "BRL",
        "quantity": 1,
        "unit_price": 45
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        pagamento = response.json()
        return pagamento["point_of_interaction"]["transaction_data"]["ticket_url"]
    return None
