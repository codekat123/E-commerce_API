from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from order.models import Order
from services import StripeService


class CreateCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            customer=request.user
        )

        if order.status != "pending":
            return Response(
                {"detail": "Order already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = StripeService.create_checkout_session(order, request.user)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        order.stripe_session_id = session.id
        order.save(update_fields=["stripe_session_id"])

        return Response({
            "checkout_url": session.url
        }, status=status.HTTP_200_OK)