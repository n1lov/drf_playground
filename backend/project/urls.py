from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from core.api.docs.views import schema_view


admin.site.site_url = None

urlpatterns = i18n_patterns(
    re_path('api/(?P<version>(v1))/', include('core.api.urls', namespace='v1')),
    path('backend/admin/', admin.site.urls),
    path('backend/grappelli/', include('grappelli.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # djoser version
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
)

urlpatterns += [
    re_path(
        r'^api/swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^api/swagger/$',
        login_required(
            schema_view.with_ui('swagger', cache_timeout=0),
            login_url=reverse_lazy('swagger-login'),
        ),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^api/redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
