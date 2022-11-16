from django.test import TestCase

from core.models.config import (USER_ROLE_CUSTOMER, USER_ROLE_STAFF)
from core.tests.factories import UserCustomerFactory


class UserTestCase(TestCase):
    def test_staff_role_on_user_create(self):
        user = UserCustomerFactory()
        self.assertEqual(user.role, USER_ROLE_CUSTOMER)
        user.is_staff = True
        user.save()
        self.assertEqual(user.role, USER_ROLE_STAFF)
