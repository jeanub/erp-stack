from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_authenticated and req.user.role == "admin")

class IsSupervisorOrAdmin(BasePermission):
    def has_permission(self, req, view):
        return bool(req.user and req.user.is_authenticated and req.user.role in {"supervisor","admin"})

class ReadOnlyOrSupervisorUp(BasePermission):
    def has_permission(self, req, view):
        if req.method in SAFE_METHODS:
            return True
        return bool(req.user and req.user.is_authenticated and req.user.role in {"supervisor","admin"})
