from django.contrib import admin
from core.models import (Bond, Stock, IdentifiedAssetProfile)


@admin.register(IdentifiedAssetProfile)
class IdentifiedAssetProfileAdmin(admin.ModelAdmin):
    list_display = (
        'isin',
        'is_active'
    )
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
    )


@admin.register(Bond)
class BondAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'asset_profile_isin',
        'custom_bonds_field'
    )
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
    )

    @admin.display(description='ISIN')
    def asset_profile_isin(self, obj):
        return obj.asset_profile.isin


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'asset_profile_isin',
        'custom_stocks_field'
    )
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by'
    )

    @admin.display(description='ISIN')
    def asset_profile_isin(self, obj):
        return obj.asset_profile.isin
