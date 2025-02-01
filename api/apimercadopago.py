import mercadopago
import time


def gerar_link_pagamento():
    sdk = mercadopago.SDK("ENV_ACCESS_TOKEN")

    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': f'payment-{time.time()}'
    }

    payment_data = {
        "transaction_amount": 40,
        "description": "Chatbot Gênesis",
        "payment_method_id": "pix",
    }

    payment_response = sdk.payment().create(payment_data, request_options)
    payment = payment_response["response"]

    # Novo caminho para acessar transaction_data
    transaction = payment.get("point_of_interaction",
                              {}).get("transaction_data", {})

    if not transaction:
        raise KeyError("transaction_data não encontrado na resposta da API")

    link_iniciar_pagamento = transaction.get("ticket_url")

    if not link_iniciar_pagamento:
        raise KeyError("ticket_url não encontrado na resposta da API")

    return link_iniciar_pagamento
