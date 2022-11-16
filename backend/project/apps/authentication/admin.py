from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            _('Auth'),
            {
                'fields': ('email', 'password')
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('role', 'is_staff', 'is_superuser', 'user_permissions')
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
