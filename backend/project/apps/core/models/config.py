from django.utils.translation import gettext_lazy as _


USER_ROLE_CUSTOMER = 'customer'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_STAFF = 'staff'
USER_ROLE_CHOICES = (
    (USER_ROLE_CUSTOMER, _('Customer')),
    (USER_ROLE_MODERATOR, _('Moderator')),
    (USER_ROLE_STAFF, _('Staff')),
)
