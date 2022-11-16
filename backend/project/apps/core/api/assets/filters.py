import django_filters
from rest_framework.filters import BaseFilterBackend

from core.models.config import USER_ROLE_CUSTOMER
from core.models.asset import IdentifiedAssetProfile


class IdentifiedAssetProfileFilter(django_filters.FilterSet):
    """
    IdentifiedAssetProfile filtration
    """
    isin = django_filters.CharFilter(field_name='isin', lookup_expr='icontains')

    class Meta:
        model = IdentifiedAssetProfile
        fields = (
            'id',
            'currency',
            'isin',
            'is_active',
        )


class IdentifiedAssetProfileFilterBackend(BaseFilterBackend):
    """
    Filter out inactive asset profiles for customers
    """
    def filter_queryset(self, request, queryset, view):
        if hasattr(request.user, 'role') and request.user.role == USER_ROLE_CUSTOMER:
            return queryset.filter(is_active=True)
        return queryset


class BondFilterBackend(BaseFilterBackend):
    """
    Filter bonds by asset owners
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class StockFilterBackend(BaseFilterBackend):
    """
    Filter stocks by asset owners
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)
