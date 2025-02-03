import sqlite3
import requests
import os
from decouple import config

os.environ['ACCESS_TOKEN'] = config('ACCESS_TOKEN')

DATABASE_PATH = "databases/usuarios.sqlite"


def criar_pagamento(usuario, valor=45):
    """Cria um link de pagamento no Mercado Pago."""
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {"ACCESS_TOKEN"}",
        "Content-Type": "application/json"
    }
    payload = {
        "transaction_amount": valor,
        "description": "Acesso ao aplicativo",
        "payment_method_id": "pix",
        "payer": {"email": f"{usuario}@email.com"}
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        pagamento = response.json()
        return pagamento["point_of_interaction"]["transaction_data"]["ticket_url"]
    return None
