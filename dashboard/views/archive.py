from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from inventory.models import Product
from users.permissions import IsVendor
from django.shortcuts import get_object_or_404


class ProductArchive(GenericViewSet):

    permission_classes = [IsVendor]
    lookup_field = "uuid"

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)

    @action(detail=True, methods=["patch"])
    def archive(self, request, *args, **kwargs):
        product = self.get_object()

        if product.is_archived:
            return Response(status=status.HTTP_204_NO_CONTENT)

        product.is_archived = True
        product.save(update_fields=["is_archived"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"])
    def unarchive(self, request, *args, **kwargs):
        product = self.get_object()

        if not product.is_archived:
            return Response(status=status.HTTP_204_NO_CONTENT)

        product.is_archived = False
        product.save(update_fields=["is_archived"])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
