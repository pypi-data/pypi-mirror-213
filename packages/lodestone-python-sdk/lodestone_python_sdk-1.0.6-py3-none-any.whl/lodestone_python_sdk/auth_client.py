import json
from urllib.parse import urljoin

from requests import request

from .exceptions import AuthException


class AuthClient:
    def __init__(self, auth_host, app_key, app_secret, auth_path='account/api/v1/access-token'):
        self.auth_url = urljoin(auth_host, auth_path)
        self.app_key = app_key
        self.app_secret = app_secret

    def get_token(self):
        response = request(
            method='post',
            url=self.auth_url,
            data={'app_key': self.app_key, 'app_secret': self.app_secret}
        )
        try:
            return json.loads(response.content)['token']
        except Exception as e:
            raise AuthException(response.text)
