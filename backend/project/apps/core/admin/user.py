from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import User
from authentication.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            _('Auth'),
            {
                'fields': ('email', 'password')
            }
        ),
        (
            _('Contact info'),
            {
                'fields': ('phone',)
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('role', 'is_staff', 'is_superuser', 'user_permissions')
            }
        ),
    )
    readonly_fields = ('created_at',)

    list_display = ('email', 'created_at', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('created_at',)
