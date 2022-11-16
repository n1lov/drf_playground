import factory.fuzzy

from core.models import Exchange


class ExchangeFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    name = factory.fuzzy.FuzzyText(prefix='Exchange:', length=10)
    mic = factory.fuzzy.FuzzyText(length=12)
    country = factory.Faker('country_code', representation='alpha-2')

    class Meta:
        model = Exchange
