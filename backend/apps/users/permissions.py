from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import User


class RolePermission(BasePermission):
    """Base permission that checks the authenticated user's role."""

    allowed_roles: tuple[str, ...] = tuple()
    allow_read_only: bool = False

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS and self.allow_read_only:
            return True

        return any(user.has_role(role_code) for role_code in self.allowed_roles)


class IsAdmin(RolePermission):
    allowed_roles = (User.ADMIN,)


class IsSupervisorOrAdmin(RolePermission):
    allowed_roles = (User.SUPERVISOR, User.ADMIN)


class ReadOnlyOrSupervisorUp(RolePermission):
    allowed_roles = (User.SUPERVISOR, User.ADMIN)
    allow_read_only = True
