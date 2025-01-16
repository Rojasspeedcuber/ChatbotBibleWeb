import requests


class Auth:

    def __init__(self):
        self.__base_url = ''
        self.__auth_url = f'{self.__base_url}autentication/token/'

    def get_token(self, email, password)
