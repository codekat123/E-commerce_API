from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Order
from wallet.service import WalletService


class PayOrderAPIView(APIView):

    def post(self, request, *args, **kwargs):
    
        order = get_object_or_404(
            Order,
            id=kwargs.get("id"),
            customer=request.user
        )

        WalletService.pay_order(
            user=request.user,
            order=order
        )

        return Response(
            {"detail": "Payment processed successfully"},
            status=status.HTTP_200_OK
        )