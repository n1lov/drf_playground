from rest_framework.routers import DefaultRouter

from core.api.exchanges.views import ExchangeViewSet
from core.api.assets.views import (
    BondViewSet,
    StockViewSet,
    IdentifiedAssetProfileViewSet,
)


app_name = 'api'

swagger_router = DefaultRouter()
swagger_router.register('bonds', BondViewSet, basename='bonds')
swagger_router.register('stocks', StockViewSet, basename='stocks')
swagger_router.register('exchanges', ExchangeViewSet, basename='exchanges')
swagger_router.register(
    'identified-asset-profiles',
    IdentifiedAssetProfileViewSet,
    basename='identified-asset-profiles'
)

swagger_patterns = swagger_router.urls


router = DefaultRouter()
# router.register('users', UserViewSet, basename='users')
router.register('bonds', BondViewSet, basename='bonds')
router.register('stocks', StockViewSet, basename='stocks')
router.register('exchanges', ExchangeViewSet, basename='exchanges')
router.register(
    'identified-asset-profiles',
    IdentifiedAssetProfileViewSet,
    basename='identified-asset-profiles'
)

urlpatterns = router.urls
