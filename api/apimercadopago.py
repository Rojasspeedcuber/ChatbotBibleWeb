from decouple import config
import mercadopago
import os

os.environ['APIM_KEY'] = config('APIM_KEY')


def gerar_link_pagamento():
    sdk = mercadopago.SDK("TEST_APIM_KEY")

    request = {
        "items": [
            {
                "id": "1",
                "title": "Chatbot Gênesis WEB",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 40,
            },
        ],
        "payment_methods": {
            "default_payment_method_id": "bank_transfer"
        }
    }

    preference_response = sdk.preference().create(request)
    preference = preference_response["response"]
    link_iniciar_pagamento = preference["init_point"]

    return link_iniciar_pagamento
