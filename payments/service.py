import requests
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')


def criar_cupom():
    """Cria um cupom de desconto no Mercado Pago."""
    url = "https://api.mercadopago.com/v1/campaigns"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": "OIKOS",
        "percent_off": 25,
        "total_coupon_limit": 5,
        "payment_methods": [
            {"type": "pix"}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Cupom criado com sucesso!")
        return response.json()
    else:
        print(f"Erro ao criar cupom: {response.status_code}")
        print(response.json())
        return None


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
        "back_urls": {
            # URL para quando o pagamento for bem-sucedido
            "success": "auto_return",
            "failure": "auto_return",  # URL para quando o pagamento falhar
            # URL para quando o pagamento estiver pendente
            "pending": "auto_return"
        },
        "auto_return": "all",  # Redireciona automaticamente após o pagamento ser aprovado
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


criar_cupom()
