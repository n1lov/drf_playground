from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from core.tests.api.api_client import JWTClient


User = get_user_model()


class TestSometing(APITestCase):
    client_class = JWTClient

    @classmethod
    def setUpTestData(cls):
        cls.email = 'test@mail.com'
        cls.password = 'test'

    def login_user(self, email=None, password=None):
        url = reverse('token_obtain_pair')
        return self.client.post(
            url,
            {
                'email': email or self.username,
                'password': password or self.password
            }
        )

    def test_jwt_token_obtain_pair(self):
        user = User.objects.create_user(self.email, self.password)
        response = self.login_user(email=user.email, password=self.password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.login_user(email='nonexistinguser@mail.com', password=self.password)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
