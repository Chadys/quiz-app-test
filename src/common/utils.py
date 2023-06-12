from django.conf import settings
from django.urls import re_path, include


def add_api_url(urlpatterns: list, version=None) -> list:
    if version is None:
        version = settings.API_VERSION
    return [
        re_path(
            rf"^{settings.API_URL_PREFIX}(?P<version>{version})/",
            include(urlpatterns),
        )
    ]
