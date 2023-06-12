from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import (
    JWTTokenUserAuthentication,
)
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _

from .token_user import TokenUserWithPermissions


class JWTTokenUserWithPermissionsAuthentication(JWTTokenUserAuthentication):
    """
    Override of JWTTokenUserAuthentication to add user permissions
    """

    def get_user(self, validated_token):
        """
        Returns a stateless user object which is backed by the given validated
        token.
        """
        if api_settings.USER_ID_CLAIM not in validated_token:
            # The TokenUser class assumes tokens will have a recognizable user
            # identifier claim.
            raise InvalidToken(_("Token contained no recognizable user identification"))

        return TokenUserWithPermissions(validated_token)


class JWTTokenUserWithPermissionsScheme(SimpleJWTScheme):
    target_class = "common.authentication.JWTTokenUserWithPermissionsAuthentication"
