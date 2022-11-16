from django.test import TestCase

from core.tests.factories import ExchangeFactory


class ExchangeTestCase(TestCase):
    def test_mic_uppercase_strip_on_object_create(self):
        mic_lowercase = ' abcde '
        exchange = ExchangeFactory()
        exchange.mic = mic_lowercase
        exchange.save()
        self.assertEqual(exchange.mic, mic_lowercase.upper().strip())
