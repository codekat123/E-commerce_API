from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from users.permissions import IsStaff, IsAdmin
from inventory.models import Product


class ActivateProductView(APIView):
    permission_classes = [IsAdmin | IsStaff]

    @transaction.atomic
    def post(self, request, uuid, *args, **kwargs):
        product = get_object_or_404(Product, uuid=uuid)

        if product.is_active:
            return Response(
                {"detail": "Product is already active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.is_active = True
        product.save(update_fields=["is_active"])

        return Response(
            {"detail": "Product activated successfully."},
            status=status.HTTP_200_OK,
        )

class DeactivateProductView(APIView):
    permission_classes = [IsAdmin | IsStaff]


    
    @transaction.atomic
    def post(self, request, uuid, *args, **kwargs):
        product = get_object_or_404(Product, uuid=uuid)

        if not product.is_active:
            return Response(
                {"detail": "Product is already inactive."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.is_active = False
        product.save(update_fields=["is_active"])

        return Response(
            {"detail": "Product deactivated successfully."},
            status=status.HTTP_200_OK,
        )
