from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ...models import Vendor, Client
from ...serializers import (
    ClientUpdateSerializer,
    VendorUpdateSerializer,
)

USER_PROFILE_CONFIG = {
    Vendor: {
        "model": Vendor,
        "serializer": VendorUpdateSerializer,
    },
    Client: {
        "model": Client,
        "serializer": ClientUpdateSerializer,
    },
}


class ProfileUpdateAPIView(UpdateAPIView):


    def _get_user_config(self):
        user = self.request.user

        for user_class, config in USER_PROFILE_CONFIG.items():
            if isinstance(user, user_class):
                return config
    
        raise ValidationError("Unsupported user type.")

    def get_object(self):
        config = self._get_user_config()
        return get_object_or_404(config["model"], pk=self.request.user.pk)

    def get_serializer_class(self):
        config = self._get_user_config()
        return config["serializer"]
