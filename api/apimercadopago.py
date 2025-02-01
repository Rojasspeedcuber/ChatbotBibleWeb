import mercadopago
import os
from decouple import config

os.environ['APIM_KEY'] = config('APIM_KEY')


def gerar_link_pagamento():
    sdk = mercadopago.SDK("APIM_KEY")

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
    }

    result = sdk.preference().create(request)
    preference = result["response"]
    return preference["init_point"]
