import mercadopago


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
    link_iniciar_pagamento = preference["init_point"]
    return link_iniciar_pagamento
