from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AbstractHistory(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('created by'),
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_created_by',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('updated by'),
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_updated_by',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
