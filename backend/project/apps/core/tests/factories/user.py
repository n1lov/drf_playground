import factory

from django.contrib.auth import get_user_model
from core.models.config import (USER_ROLE_CUSTOMER, USER_ROLE_MODERATOR, USER_ROLE_STAFF)


class AbstractUserFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    email = factory.Faker('ascii_free_email')
    password = factory.Faker('password', length=12, digits=True, upper_case=True, lower_case=True)
    phone = factory.Faker('phone_number')

    class Meta:
        abstract = True
        model = get_user_model()


class UserStaffFactory(AbstractUserFactory):
    role = USER_ROLE_STAFF
    is_staff = True


class UserModeratorFactory(AbstractUserFactory):
    role = USER_ROLE_MODERATOR


class UserCustomerFactory(AbstractUserFactory):
    role = USER_ROLE_CUSTOMER
