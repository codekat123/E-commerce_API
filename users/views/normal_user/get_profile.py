from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ...serializers import VendorRetrieveSerializer , ClientRetrieveSerializer
from ...models import Vendor,Client


USER_SERIALIZER_MAP = {
    Vendor: VendorRetrieveSerializer,
    Client: ClientRetrieveSerializer,
}


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        user = self.request.user

        for model, serializer in USER_SERIALIZER_MAP.items():
            if isinstance(user, model):
                return serializer

        raise ValidationError("Unsupported user type.")

    def get_object(self):
        return self.request.user
