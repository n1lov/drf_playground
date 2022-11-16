from rest_framework import viewsets

from core.utils.permissions import IsStaff
from core.api.exchanges.serializers import ExchangeSerializer
from core.models import Exchange


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = (IsStaff,)
