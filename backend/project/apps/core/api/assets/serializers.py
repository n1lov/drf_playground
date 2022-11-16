from rest_framework import serializers

from core.models.config import USER_ROLE_CUSTOMER
from core.models.asset import (Bond, Stock, IdentifiedAssetProfile)


class IdentifiedAssetProfileSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(IdentifiedAssetProfileSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        # hide is_active field for customers
        if hasattr(user, 'role') and user.role == USER_ROLE_CUSTOMER:
            if hasattr(self, 'fields'):
                self.fields.pop('is_active')

    class Meta:
        model = IdentifiedAssetProfile
        fields = (
            'id',
            'currency',
            'isin',
            'is_active',
        )


class BondSerializer(serializers.ModelSerializer):

    isin = serializers.UUIDField(source='asset_profile.isin', read_only=True)

    class Meta:
        model = Bond
        fields = (
            'id',
            'exchange',
            'notes',
            'isin',
            'custom_bonds_field',
        )


class StockSerializer(serializers.ModelSerializer):

    isin = serializers.UUIDField(source='asset_profile.isin', read_only=True)

    class Meta:
        model = Stock
        fields = (
            'id',
            'exchange',
            'notes',
            'isin',
            'custom_stocks_field',
        )
