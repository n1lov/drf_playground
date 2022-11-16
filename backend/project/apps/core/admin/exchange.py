from django.contrib import admin
from core.models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'mic')
    autocomplete_lookup_fields = {
        'fk': [
            'title',
        ],
    }
