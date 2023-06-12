from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenViewBase,
)

from .serializers import (
    FullInfoTokenObtainPairSerializer,
    DbSyncTokenRefreshSerializer,
    BlacklistRefreshSerializer,
)


def health_check(request):
    return Response({})


class FullInfoTokenObtainPairView(TokenObtainPairView):
    serializer_class = FullInfoTokenObtainPairSerializer


class DbSyncTokenRefreshView(TokenRefreshView):
    serializer_class = DbSyncTokenRefreshSerializer


class BlacklistRefreshView(TokenViewBase):
    serializer_class = BlacklistRefreshSerializer
