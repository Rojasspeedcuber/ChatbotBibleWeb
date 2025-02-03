import requests
from decouple import config


def criar_pagamento():
    url = "https://api.mercadopago.com/checkout/preferences"
    headers = {
        "Authorization": f"Bearer {config('ACCESS_TOKEN')}",
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
                # Se não quiser permitir boletos, exclua o tipo "ticket"
                {"id": "ticket"}
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
        # Em caso de erro, exibe os detalhes da resposta para depuração
        print(f"Erro ao criar pagamento: {response.status_code}")
        print(f"Detalhes do erro: {response.text}")
        return None
