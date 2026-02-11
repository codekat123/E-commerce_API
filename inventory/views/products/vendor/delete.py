from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404

from ....models import Product
from users.permissions import IsVendor, IsAdmin, IsStaff


class ProductDestroyAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsVendor | IsAdmin | IsStaff]
    lookup_field = "uuid"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return self.queryset

        return self.queryset.filter(vendor=user)
