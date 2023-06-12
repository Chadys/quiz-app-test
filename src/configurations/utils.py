import enum
from rest_framework.renderers import BrowsableAPIRenderer


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """Renders the browsable api, but excludes the forms."""

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx["display_edit_forms"] = False
        ctx["filter_form"] = None
        return ctx

    def show_form_for_method(self, view, method, request, obj):
        """We never want to do this! So just return False."""
        return False

    def get_rendered_html_form(self, data, view, method, request):
        """Why render _any_ forms at all. This method should return
        rendered HTML, so let's simply return an empty string.
        """
        return ""

    def get_filter_form(self, data, view, request):
        return None


class EnvMode(enum.Enum):
    TEST = enum.auto()
    DEV = enum.auto()
    QA = enum.auto()
    PROD = enum.auto()
    DEMO = enum.auto()


def add_ending_slash(url: str) -> str:
    if url.endswith("/"):
        return url
    return f"{url}/"


def remove_ending_slash(url: str) -> str:
    if url.endswith("/"):
        return url[:-1]
    return url
