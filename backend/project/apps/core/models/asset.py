from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings

from core.models.abstract import AbstractHistory
from core.utils.const import CURRENCY_CHOICES


class IdentifiedAssetProfile(AbstractHistory):
    currency = models.CharField(
        _('currency'),
        max_length=3,
        help_text=_('Currency'),
        choices=CURRENCY_CHOICES,
    )
    isin = models.CharField(
        _('isin'),
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
        ],
        help_text=_('International Securities Identification Number'),
        unique=True
    )
    is_active = models.BooleanField(
        _('is_active'),
        default=True,
        help_text=_('is_active flag'),
    )

    # + universal category -> categories
    # + issuer -> issuers
    # + ... and so on

    def __str__(self):
        return f'ISIN:{self.isin}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.isin = self.isin.upper().strip()
        return super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def force_delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


class AbstractIdentifiedAsset(AbstractHistory):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=True
    )
    # IdentifiedAssetProfile model set is_active=False on "delete" trigger
    asset_profile = models.ForeignKey(
        'core.IdentifiedAssetProfile',
        verbose_name=_('Asset profile'),
        related_name='%(class)s_asset_profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        help_text=_('Asset profile (generic)')
    )
    exchange = models.ForeignKey(
        'core.Exchange',
        verbose_name=_('Exchange'),
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('Exchange name')
    )
    notes = models.TextField(
        _('User notes'),
        blank=True,
        max_length=2000,
        help_text=_('Notes')
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'Exchange:{self.exchange.name} ISIN:{self.asset_profile.isin}'


class Bond(AbstractIdentifiedAsset):
    custom_bonds_field = models.CharField(
        _('custom field for bonds'),
        blank=True,
        max_length=100,
        help_text=_('custom field for bonds')
    )

    class Meta:
        unique_together = ('asset_profile', 'exchange', 'user')
        verbose_name = _('Bond')
        verbose_name_plural = _('Bonds')


class Stock(AbstractIdentifiedAsset):
    custom_stocks_field = models.CharField(
        _('custom field for stocks'),
        blank=True,
        max_length=100,
        help_text=_('custom field for stocks')
    )

    class Meta:
        unique_together = ('asset_profile', 'exchange', 'user')
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
