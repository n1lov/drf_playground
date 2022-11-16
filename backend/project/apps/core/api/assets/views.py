from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from core.api.assets.filters import (
    IdentifiedAssetProfileFilter,
    BondFilterBackend,
    StockFilterBackend,
    IdentifiedAssetProfileFilterBackend,
)
from core.api.assets.serializers import (
    BondSerializer,
    StockSerializer,
    IdentifiedAssetProfileSerializer,
)
from core.utils.permissions import (IsStaff, IsCustomer, IsModerator, IsCustomerReadOnly)
from core.models import (Bond, Stock, IdentifiedAssetProfile)


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
    filter_backends = (BondFilterBackend, DjangoFilterBackend,)
    permission_classes = (IsStaff | IsCustomer,)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = (StockFilterBackend, DjangoFilterBackend,)
    permission_classes = (IsStaff | IsCustomer,)


class IdentifiedAssetProfileViewSet(viewsets.ModelViewSet):
    queryset = IdentifiedAssetProfile.objects.all()
    serializer_class = IdentifiedAssetProfileSerializer
    filterset_class = IdentifiedAssetProfileFilter
    filter_backends = (IdentifiedAssetProfileFilterBackend, DjangoFilterBackend,)
    permission_classes = (IsStaff | IsModerator | IsCustomerReadOnly,)
