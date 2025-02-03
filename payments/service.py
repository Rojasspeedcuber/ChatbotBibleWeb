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
        "transaction_amount": 45,  # Valor da transação
        "description": "Acesso ao aplicativo",  # Descrição do pagamento
        # Método de pagamento, como "pix", "credit_card", etc.
        "payment_method_id": "pix",
        "payer": {
            # E-mail do pagador (pode ser omitido se você não souber)
            "email": "exemplo@dominio.com"
        }
    }

    # Envia a requisição POST para criar o pagamento
    response = requests.post(url, json=payload, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 201:
        pagamento = response.json()
        # Retorna a URL do boleto ou link de pagamento
        return pagamento["point_of_interaction"]["transaction_data"]["ticket_url"]
    else:
        # Em caso de erro, exibe os detalhes da resposta para depuração
        print(f"Erro ao criar pagamento: {response.status_code}")
        print(f"Detalhes do erro: {response.text}")
        return None
