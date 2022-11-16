from django.urls import include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from core.api.urls import swagger_patterns


schema_view = get_schema_view(
    openapi.Info(
        title="App API",
        default_version='v1',
    ),
    public=False,
    patterns=[re_path(r'en/api/v1/', include(swagger_patterns))],
    permission_classes=(IsAuthenticated,),
)
