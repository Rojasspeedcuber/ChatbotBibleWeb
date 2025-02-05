import requests  # Certifique-se de importar requests
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
            "frequency": 12,  # 4 meses
            "frequency_type": "months",
            "transaction_amount": 5.00,  # Valor da assinatura
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
