from .settings import *

INSTALLED_APPS.extend(
    [
        "django_extensions",
        "debug_toolbar",
        "django_watchfiles",
        "django_browser_reload",
    ]
)

INTERNAL_IPS = ["127.0.0.1"]
# MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MIDDLEWARE.insert(-2, "django_browser_reload.middleware.BrowserReloadMiddleware")
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True
    if DEBUG
    else False,  # this is necessary because we can't predict INTERNAL_IPS on docker
}


# use rich to format error output
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "rich": {"datefmt": "[%X]", "format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
            "show_path": False,
            "enable_link_path": False,
        },
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
