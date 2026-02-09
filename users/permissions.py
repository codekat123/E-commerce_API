from rest_framework.permissions import BasePermission
from .models import Admin, Staff, Vendor, Client


class IsUserType(BasePermission):
    allowed_types = ()

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and isinstance(user, self.allowed_types)
        )


class IsAdmin(IsUserType):
    allowed_types = (Admin,)


class IsStaff(IsUserType):
    allowed_types = (Staff,)


class IsClient(IsUserType):
    allowed_types = (Client,)


class IsVendor(IsUserType):
    allowed_types = (Vendor,)
