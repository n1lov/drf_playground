from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import config
from authentication.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(
        _('uuid'),
        default=uuid4,
        editable=False,
        unique=True,
        help_text=_('User uuid')
    )
    phone = models.CharField(
        _('phone'),
        max_length=50,
        blank=True,
        help_text=_('Phone number')
    )
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=config.USER_ROLE_CHOICES,
        default=config.USER_ROLE_CUSTOMER,
        help_text=_('User role')
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = config.USER_ROLE_STAFF
        super().save(*args, **kwargs)
