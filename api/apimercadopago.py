import mercadopago


def gerar_link_pagamento():
    sdk = mercadopago.SDK(
        "APP_USR-6958238556951676-012309-0e24e947de4f94ca0959a404c3af4582-446605533")

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
