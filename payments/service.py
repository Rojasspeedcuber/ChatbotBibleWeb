import requests
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')


def criar_assinatura(email):
    """Cria uma assinatura no Mercado Pago com duração de 4 meses."""

    url = "https://api.mercadopago.com/preapproval"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "reason": "Assinatura do Chatbot Gênesis",
        "auto_recurring": {
            "frequency": 4,  # 4 meses
            "frequency_type": "months",
            "transaction_amount": 30.00,  # Valor da assinatura
            "currency_id": "BRL",
        },
        "payer_email": email,  # E-mail do assinante
        "back_url": "https://chatbotgenesisweb.streamlit.app/",
        "status": "pending"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        assinatura = response.json()
        return assinatura.get("init_point")  # Link para o usuário assinar
    else:
        print(f"Erro ao criar assinatura: {response.status_code}")
        print(response.json())
        return None


def verificar_assinatura(preapproval_id):
    """Verifica se a assinatura do usuário ainda está ativa."""

    url = f"https://api.mercadopago.com/preapproval/{preapproval_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assinatura = response.json()
        status = assinatura.get("status")

        # Se a assinatura estiver ativa, permitir o acesso
        return status in ["authorized", "paused"]
    else:
        print(f"Erro ao verificar assinatura: {response.status_code}")
        return False
