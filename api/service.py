import requests


class Auth:

    def __init__(self):
        self.__base_url = 'https://api.mercadopago.com'
        self.__auth_url = f'{self.__base_url}/v1/payments'

    def get_token(self, username, password):
        auth_payload = {
            'username': username,
            'password': password
        }
        auth_response = requests.post(
            self.__auth_url,
            data=auth_payload
        )
        if auth_response.status_code == 200:
            return auth_response.json()
        return {'error': f'Erro ao autenticar. Status code: {auth_response.status_code}'}
