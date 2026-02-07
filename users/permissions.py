from rest_framework.permissions import BasePermission
from .models import Admin , Staff

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.__class__.__name__ == "Admin"
        )


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.__class__.__name__ == "Staff"
        )
