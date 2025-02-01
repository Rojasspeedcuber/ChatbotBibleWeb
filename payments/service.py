import sqlite3
import requests
import os
from decouple import config

os.environ['ACCESS_TOKEN'] = config('ACCESS_TOKEN')

DATABASE_PATH = "databases/usuarios.sqlite"


def criar_pagamento(usuario, valor=45):
    """Cria um link de pagamento no Mercado Pago."""
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {"ACCESS_TOKEN"}",
        "Content-Type": "application/json"
    }
    payload = {
        "transaction_amount": valor,
        "description": "Acesso ao aplicativo",
        "payment_method_id": "pix",
        "payer": {"email": f"{usuario}@email.com"}
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        pagamento = response.json()
        salvar_pagamento(usuario, pagamento["id"], pagamento["status"])
        return pagamento["point_of_interaction"]["transaction_data"]["ticket_url"]
    return None


def salvar_pagamento(usuario, pagamento_id, status):
    """Salva o status do pagamento no banco de dados."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            pagamento_id TEXT,
            status TEXT
        )
    """)
    cursor.execute("INSERT INTO pagamentos (usuario, pagamento_id, status) VALUES (?, ?, ?)",
                   (usuario, pagamento_id, status))
    conn.commit()
    conn.close()


def verificar_status_pagamento(usuario):
    """Verifica no banco de dados se o usuário já pagou."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status FROM pagamentos WHERE usuario = ? ORDER BY id DESC LIMIT 1", (usuario,))
    status = cursor.fetchone()
    conn.close()
    return status and status[0] == "approved"
