from .base import *  # noqa


SHOW_SWAGGER = env.bool("SHOW_SWAGGER", default=DEBUG)
INTERACTIVE_SWAGGER = env.bool("INTERACTIVE_SWAGGER", default=SHOW_SWAGGER)

# django rest framework
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "common.authentication.JWTTokenUserWithPermissionsAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

API_URL_PREFIX = add_ending_slash(env.str("API_URL_PREFIX", default="api/"))
API_VERSION = "v1"


if SHOW_SWAGGER:
    # needed to authenticate with browsable and swagger API
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(
        "rest_framework.authentication.SessionAuthentication"
    )
    REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
    SPECTACULAR_SETTINGS = {
        "SCHEMA_PATH_PREFIX": f"/{API_URL_PREFIX}v\d+",
        "TITLE": f"{SITE_NAME} {API_VERSION} API",
        "DESCRIPTION": f"{SITE_NAME} {API_VERSION} API",
        "VERSION": None,
        "AUTHENTICATION_WHITELIST": [
            "common.authentication.JWTTokenUserWithPermissionsAuthentication"
        ],
        "APPEND_COMPONENTS": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                }
            }
        },
        "SECURITY": [
            {
                "ApiKeyAuth": [],
            }
        ],
        "COMPONENT_SPLIT_REQUEST": True,
        "SWAGGER_UI_SETTINGS": {
            "deepLinking": True,
            "persistAuthorization": True,
            "filter": True,
        },
    }
    if INTERACTIVE_SWAGGER:
        REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
            # "rest_framework.renderers.BrowsableAPIRenderer"
            "common.renderers.BrowsableAPIRendererWithoutForms"
        )
        SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"]["tryItOutEnabled"] = True
    else:
        SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"]["supportedSubmitMethods"] = []

# djangorestframework-simplejwt
SIMPLE_JWT = {
    # env timedelta assumes value is an integer in seconds
    "ACCESS_TOKEN_LIFETIME": env.timedelta(
        "ACCESS_TOKEN_LIFETIME", default=432000 if DEBUG else 300
    ),  # dev: 5 days, prod: 5min
    "REFRESH_TOKEN_LIFETIME": env.timedelta(
        "REFRESH_TOKEN_LIFETIME", default=864000 if DEBUG else 14400
    ),  # dev: 10 days, prod: 4h
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS512",
    "SIGNING_KEY": env.str("SIMPLE_JWT_SIGNING_KEY"),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": env.list(
        "SIMPLE_JWT_AUTH_HEADER_TYPES", subcast=str, default=("Bearer",)
    ),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}
