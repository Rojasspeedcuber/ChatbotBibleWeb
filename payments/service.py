import requests
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')


def criar_assinatura(email):
    """Cria uma assinatura no Mercado Pago com duração de 12 meses."""

    url = "https://api.mercadopago.com/preapproval"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "reason": "Assinatura do Chatbot Gênesis",
        "auto_recurring": {
            "frequency": 12,  # 12 meses
            "frequency_type": "months",
            "transaction_amount": 5.00,  # Valor da assinatura
            "currency_id": "BRL",
            # Data de início da assinatura (ajuste conforme necessário)
            "start_date": "2025-02-20T00:00:00Z",
            # Data de término (ajuste conforme necessário)
            "end_date": "2026-02-20T00:00:00Z",
        },
        "payer_email": email,  # E-mail do assinante
        "back_url": "https://chatbotgenesisweb.rojasdev.site/",
        "status": "preapproval"
    }

    # Fazendo o pedido para criar a assinatura
    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            assinatura = response.json()
            # Link para o usuário assinar
            link_pagamento = assinatura.get("init_point")

            if link_pagamento:
                return link_pagamento
            else:
                print("Erro: Link de pagamento não encontrado na resposta.")
                return None
        else:
            print(f"Erro ao criar assinatura: {response.status_code}")
            print(response.json())
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


def verificar_assinatura(preapproval_id):
    """Verifica se a assinatura do usuário ainda está ativa."""

    url = f"https://api.mercadopago.com/preapproval/{preapproval_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança erro em caso de falha HTTP

        assinatura = response.json()
        status = assinatura.get("status")

        if status is None:
            print("❌ Erro: Resposta inesperada da API do Mercado Pago.")
            return False

        if status == "authorized":
            print("✅ Assinatura ativa.")
            return True
        else:
            print(f"⚠️ Assinatura inativa. Status: {status}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao verificar assinatura: {e}")
        return False
