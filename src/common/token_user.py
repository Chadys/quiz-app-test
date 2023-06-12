from functools import cached_property

from rest_framework_simplejwt.models import TokenUser
from django.contrib.auth import get_user_model


# noinspection PyAbstractClass
class TokenUserWithPermissions(TokenUser):
    """
    An override of TokenUser to add user permissions
    """

    @cached_property
    def username(self):
        return self.token.get(get_user_model().USERNAME_FIELD, "")

    @cached_property
    def email(self):
        return self.token.get("email", "")

    @cached_property
    def permissions(self):
        return set(self.token.get("permissions", ""))

    def get_all_permissions(self, obj=None):
        return self.permissions

    def get_user_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return self.is_active and (
            self.is_superuser or perm in self.get_all_permissions(obj=obj)
        )

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if user_obj has any permissions in the given app_label.
        """
        return self.is_active and (
            self.is_superuser
            or any(
                perm[: perm.index(".")] == app_label
                for perm in self.get_all_permissions()
            )
        )

    @cached_property
    def db_user(self):
        return User.objects.get(pk=self.pk)
