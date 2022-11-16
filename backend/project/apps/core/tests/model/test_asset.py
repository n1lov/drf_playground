from django.test import TestCase

from core.tests.factories import IdentifiedAssetProfileFactory


class IdentifiedAssetProfileTestCase(TestCase):
    def test_isin_uppercase_strip_on_object_create(self):
        lowercased_isin = 'abc203918282 '
        identified_asset_profile = IdentifiedAssetProfileFactory()
        identified_asset_profile.isin = lowercased_isin
        identified_asset_profile.save()
        self.assertEqual(identified_asset_profile.isin, lowercased_isin.upper().strip())

    def test_inactive_profile_on_object_delete(self):
        identified_asset_profile = IdentifiedAssetProfileFactory()
        self.assertTrue(identified_asset_profile.is_active)
        identified_asset_profile.delete()
        identified_asset_profile.refresh_from_db()
        self.assertFalse(identified_asset_profile.is_active)
