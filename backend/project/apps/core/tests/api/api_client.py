from django.conf import settings

from rest_framework.test import APIClient

from core.tests.utils import get_jwt_token
from core.models import User


class JWTClient(APIClient):
    _headers = {}

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs, **self._headers)

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs, **self._headers)

    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs, **self._headers)

    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs, **self._headers)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs, **self._headers)

    def login(self, user: User):
        token = get_jwt_token(user).access_token
        self._headers = {
            'HTTP_AUTHORIZATION': f'{settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0]} {token}'
        }

    def logout(self):
        self._credentials = {}
        self._headers = {}
        self.handler._force_user = None
        self.handler._force_token = None
