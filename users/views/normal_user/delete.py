from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied

from ...models import Vendor, Client


class SelfDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if not isinstance(user, (Vendor, Client)):
            raise PermissionDenied("You can't delete this account.")

        return user
