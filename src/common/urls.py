from django.conf import settings
from django.urls import path, re_path

from .views import (
    FullInfoTokenObtainPairView,
    DbSyncTokenRefreshView,
    BlacklistRefreshView,
    health_check,
)

urlpatterns = [
    path("health_check/", health_check, name="health-check"),
    # Auth
    # re_path(
    #     r"^token/?$",
    #     FullInfoTokenObtainPairView.as_view(),
    #     name="token_obtain_pair",
    # ),
    # re_path(
    #     r"^token/refresh/?$", DbSyncTokenRefreshView.as_view(), name="token_refresh"
    # ),
    # re_path(
    #     r"^token/blacklist/?$", BlacklistRefreshView.as_view(), name="blacklist_refresh"
    # ),
]


if settings.SHOW_SWAGGER:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
    )

    urlpatterns.extend(
        [
            path("schema/", SpectacularAPIView.as_view(), name="openapi-schema"),
            path(
                "schema/swagger-ui/",
                SpectacularSwaggerView.as_view(url_name="openapi-schema"),
                name="swagger-ui",
            ),
        ]
    )
