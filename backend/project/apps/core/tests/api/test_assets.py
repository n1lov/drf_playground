from typing import Dict, List

from django.urls import reverse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import IdentifiedAssetProfile
from core.tests.factories import (
    UserCustomerFactory,
    UserModeratorFactory,
    UserStaffFactory,
    IdentifiedAssetProfileFactory,
    ExchangeFactory,
    BondFactory,
    # StockFactory # same as for bonds, the project is just a showcase
)

from core.tests.api.api_client import JWTClient


class TestSometing(APITestCase):
    client_class = JWTClient

    @classmethod
    def setUpTestData(cls):
        cls.version = 'v1'

        cls.user_customer1 = UserCustomerFactory()
        cls.user_customer2 = UserCustomerFactory()
        cls.user_moderator1 = UserModeratorFactory()
        cls.user_moderator2 = UserModeratorFactory()
        cls.user_staff = UserStaffFactory()

        cls.exchange1 = ExchangeFactory()
        cls.exchange2 = ExchangeFactory()

        cls.id_asset_profile = IdentifiedAssetProfileFactory(
            created_by=cls.user_moderator1,
            updated_by=cls.user_moderator1
        )

        cls.id_asset_profile_inactive = IdentifiedAssetProfileFactory(
            created_by=cls.user_moderator1,
            updated_by=cls.user_moderator1,
            is_active=False
        )

        cls.user_customer1_bond_exchange1 = BondFactory(
            created_by=cls.user_customer1,
            updated_by=cls.user_customer1,
            asset_profile=cls.id_asset_profile,
            exchange=cls.exchange1,
            user=cls.user_customer1
        )

        cls.user_customer1_bond_exchange2 = BondFactory(
            created_by=cls.user_customer1,
            updated_by=cls.user_customer1,
            asset_profile=cls.id_asset_profile,
            exchange=cls.exchange2,
            user=cls.user_customer1
        )

        cls.user_customer2_bond_exchange1 = BondFactory(
            created_by=cls.user_customer2,
            updated_by=cls.user_customer2,
            asset_profile=cls.id_asset_profile,
            exchange=cls.exchange1,
            user=cls.user_customer2
        )

        # same for stocks (the project is just a showcase)
        cls.bonds_list_url = reverse('api:bonds-list', args=(cls.version,))
        cls.bonds_detail_url = reverse('api:bonds-detail', args=(cls.version, cls.user_customer2_bond_exchange1.id))
        cls.bonds_serializer_keys = {
            'id',
            'exchange',
            'notes',
            'isin',
            'custom_bonds_field'
        }

        cls.identified_asset_profile_list_url = reverse(
            'api:identified-asset-profiles-list',
            args=(cls.version,)
        )
        cls.identified_asset_profile_detail_url = reverse(
            'api:identified-asset-profiles-detail',
            args=(cls.version, cls.id_asset_profile.id)
        )
        cls.identified_asset_profile_serializer_keys_customer_view = {
            'id',
            'currency',
            'isin',
        }

        cls.identified_asset_profile_serializer_keys_moderator_view = {
            'id',
            'currency',
            'isin',
            'is_active'
        }

    def test_non_authorized(self):
        response = self.client.get(self.bonds_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(self.bonds_list_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(self.bonds_list_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # same for stocks (the project is just a showcase)
    def test_bonds_customer_filtration_and_pagination(self):
        self.client.login(self.user_customer1)
        response = self.client.get(self.bonds_list_url, format='json')
        self.assertTrue({"count", "results", "previous", "next"}.issubset(response.data.keys()))
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0].keys(), self.bonds_serializer_keys)
        # user_customer2_bond_exchange1 is filtered out in the list view
        self.assertEqual(
            {result['id'] for result in response.data['results']},
            {self.user_customer1_bond_exchange1.id, self.user_customer1_bond_exchange2.id}
        )

    def test_bonds_customer_direct_access(self):
        self.client.login(self.user_customer1)
        response = self.client.get(self.bonds_detail_url, format='json')  # customer 2
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.logout()
        self.client.login(self.user_customer2)
        response = self.client.get(self.bonds_detail_url, format='json')  # customer 2
        self.assertEqual(response.data.keys(), self.bonds_serializer_keys)
        self.assertEqual(response.data['id'], self.user_customer2_bond_exchange1.id)

    def test_identified_asset_profile_customer_view(self):
        # test detail url
        self.client.login(self.user_customer1)
        response = self.client.get(self.identified_asset_profile_detail_url, format='json')
        self.assertEqual(response.data.keys(), self.identified_asset_profile_serializer_keys_customer_view)

        # test is_active filter for customers on list url
        response = self.client.get(self.identified_asset_profile_list_url, format='json')
        self.assertEqual(response.data['results'][0]['id'], self.id_asset_profile.id)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0].keys(),
            self.identified_asset_profile_serializer_keys_customer_view
        )

    def test_identified_asset_profile_moderator_view(self):
        # test detail url
        self.client.login(self.user_moderator1)
        response = self.client.get(self.identified_asset_profile_detail_url, format='json')
        self.assertEqual(response.data.keys(), self.identified_asset_profile_serializer_keys_moderator_view)

        # test is_active filter for customers on list url
        response = self.client.get(self.identified_asset_profile_list_url, format='json')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(
            response.data['results'][0].keys(),
            self.identified_asset_profile_serializer_keys_moderator_view
        )

    # test unsafe identified_asset_profile actions C(R)UD -- create, update, delete methods
    def _cud_methods(self, url: str, patch_data: Dict, post_data: Dict) -> List[Response]:
        return [
            self.client.post(url, data={}),
            self.client.put(url, data={}),
            self.client.patch(url, data={}),
            self.client.delete(url),

            self.client.post(url, data=post_data),
            self.client.put(url, data=patch_data),
            self.client.patch(url, data=patch_data),
            self.client.delete(url),
        ]

    def test_identified_asset_profile_cud_methods(self):
        patch_data = {'isin': 'UUMGCZMISIBB'}
        post_data = {'currency': 'USD', 'isin': 'UUMGCZMISXXX', 'is_active': True}
        url = self.identified_asset_profile_detail_url

        self.client.logout()
        for cud_method in self._cud_methods(url=url, patch_data=patch_data, post_data=post_data):
            self.assertEqual(cud_method.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(self.user_customer1)
        for cud_method in self._cud_methods(url=url, patch_data=patch_data, post_data=post_data):
            self.assertEqual(cud_method.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(self.user_moderator1)
        response = self.client.post(self.identified_asset_profile_list_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['currency'], post_data['currency'])
        self.assertEqual(response.data['isin'], post_data['isin'])
        self.assertEqual(response.data['is_active'], post_data['is_active'])

        created_asset_id = response.data['id']
        # moderator can update it's own asset profile
        response = self.client.patch(
            reverse('api:identified-asset-profiles-detail', args=('v1', created_asset_id)),
            data={'isin': 'UUMGCZMIQQQQ'}
        )
        self.assertEqual(response.data['isin'], 'UUMGCZMIQQQQ')

        # other moderator can also update asset profile
        self.client.login(self.user_moderator2)
        response = self.client.patch(
            reverse('api:identified-asset-profiles-detail', args=('v1', created_asset_id)),
            data={'isin': 'UUMGCZMIWWWW'}
        )
        self.assertEqual(response.data['isin'], 'UUMGCZMIWWWW')

        # set is_active = False instead of removing the record
        response = self.client.delete(reverse('api:identified-asset-profiles-detail', args=('v1', created_asset_id)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IdentifiedAssetProfile.objects.get(id=created_asset_id).is_active, False)
