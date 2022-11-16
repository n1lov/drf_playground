import factory.fuzzy

from core.tests.factories import (UserCustomerFactory, UserStaffFactory, ExchangeFactory)
from core.models.asset import AbstractIdentifiedAsset
from core.models import (Bond, Stock, IdentifiedAssetProfile)


class IdentifiedAssetProfileFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserStaffFactory)
    updated_by = factory.SubFactory(UserStaffFactory)
    isin = factory.fuzzy.FuzzyText(length=12)
    is_active = True
    currency = 'USD'

    class Meta:
        model = IdentifiedAssetProfile


class AbstractIdentifiedAssetFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserCustomerFactory)
    user = factory.SubFactory(UserCustomerFactory)
    asset_profile = factory.SubFactory(IdentifiedAssetProfileFactory)
    exchange = factory.SubFactory(ExchangeFactory)
    notes = factory.fuzzy.FuzzyText(length=150)

    class Meta:
        abstract = True
        model = AbstractIdentifiedAsset


class BondFactory(AbstractIdentifiedAssetFactory):
    custom_bonds_field = factory.fuzzy.FuzzyText(length=20)

    class Meta:
        model = Bond


class StockFactory(AbstractIdentifiedAssetFactory):
    custom_stocks_field = factory.fuzzy.FuzzyText(length=20)

    class Meta:
        model = Stock
