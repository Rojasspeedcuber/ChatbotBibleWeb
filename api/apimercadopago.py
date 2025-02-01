
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
    link_iniciar_pagamento = payment["ticket_url"]

    return link_iniciar_pagamento
