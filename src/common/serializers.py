from drf_spectacular.contrib.rest_framework_simplejwt import (
    TokenRefreshSerializerExtension,
    TokenObtainPairSerializerExtension,
)
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import get_user_model


# noinspection PyAbstractClass
class FullInfoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        if not user.is_superuser:
            # only fill permissions for non-super user else token will be too big
            # permissions list is not checked for superuser anyway
            token["permissions"] = list(user.get_all_permissions())
        return token


# noinspection PyAbstractClass
class DbSyncTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Override parent to check on user in db, to prevent desync between TokenUser and saved data.
    This is needed because with TokenUser there is never any db call,
    """

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])
        refresh = self.sync_token_user_with_db(refresh)

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)

        return data

    def sync_token_user_with_db(self, token):
        """
        Update token content with eventual db changes.
        """
        try:
            user_id = token[api_settings.USER_ID_CLAIM]
            username = token[get_user_model().USERNAME_FIELD]
        except KeyError:
            raise TokenError("Token contained no recognizable user identification")
        try:
            user = get_user_model().objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
        token["permissions"] = set()
        token = self.sync_token_user_main_attr(token, user)

        token["permissions"] = list(token["permissions"])
        return token

    @staticmethod
    def sync_token_user_main_attr(token, user):
        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        token["permissions"] |= user.get_all_permissions()
        return token


# noinspection PyAbstractClass
class BlacklistRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])
        refresh.blacklist()

        return {}


class FullInfoTokenObtainPairSerializerExtension(TokenObtainPairSerializerExtension):
    target_class = "common.serializers.FullInfoTokenObtainPairSerializer"


class BlacklistRefreshSerializerExtension(TokenRefreshSerializerExtension):
    target_class = "common.serializers.BlacklistRefreshSerializer"


class DbSyncTokenRefreshSerializerExtension(TokenRefreshSerializerExtension):
    target_class = "common.serializers.DbSyncTokenRefreshSerializer"
