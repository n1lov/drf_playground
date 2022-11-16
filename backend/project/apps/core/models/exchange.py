from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils.const import COUNTRIES_CHOICES
from simple_history.models import HistoricalRecords


class Exchange(models.Model):
    uuid = models.UUIDField(
        _('uuid'),
        default=uuid4,
        editable=False,
        unique=True,
        help_text=_('Exchange uuid')
    )
    name = models.CharField(
        _('title'),
        max_length=100,
        help_text=_('Stock exchange name')
    )
    mic = models.CharField(
        _('mic'),
        max_length=20,
        help_text=_('Market identifier code'),
        unique=True,
        error_messages={
            "unique": _("An exchange with that MIC already exists."),
        },
    )
    country = models.CharField(
        _('country'),
        max_length=2,
        help_text=_('Country'),
        choices=COUNTRIES_CHOICES
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Stock exchange')
        verbose_name_plural = _('Stock exchanges')

    def __str__(self):
        return f"{self.name} - {self.mic}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.mic = self.mic.upper().strip()
        return super().save(force_insert, force_update, using, update_fields)
