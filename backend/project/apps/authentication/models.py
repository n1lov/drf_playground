from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)

from authentication.manager import UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    Slightly changed AbstractBaseUser model
    """
    email = models.EmailField(
        _('email'),
        db_index=True,
        unique=True,
        help_text=_('Email address'),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(_('is_active'), default=True, help_text=_('is_active user status'))
    is_staff = models.BooleanField(_('is_staff'), default=False, help_text=_('is_staff user status'))
    is_superuser = models.BooleanField(_('is_superuser'), default=False, help_text=_('is_superuser user status'))
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def __str__(self):
        return self.email
