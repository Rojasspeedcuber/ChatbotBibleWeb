import requests


class Auth:
    def __init__(self, access_token):
        self.__base_url = 'https://api.mercadopago.com'
        self.__access_token = access_token

    def check_auth(self):
        """Verifica se o Access Token é válido"""
        url = f"{self.__base_url}/v1/payments"
        headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return {"status": "Autenticado com sucesso!"}
        else:
            return {"error": f"Erro ao autenticar. Código: {response.status_code} - {response.text}"}


# Exemplo de uso
ACCESS_TOKEN = "SEU_ACCESS_TOKEN"  # Substitua pelo token real
auth = Auth(ACCESS_TOKEN)
print(auth.check_auth())
