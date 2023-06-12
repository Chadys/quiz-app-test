import unicodedata

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


def remove_accents(text: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def convert_to_ascii(text: str) -> str:
    return remove_accents(text).encode("ascii", "ignore").decode("ascii")
