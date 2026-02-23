from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from order.models import Order
from services import StripeService


class CreateCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, customer=request.user)

        if order.status != "pending":
            return Response({"detail": "Order already processed"}, status=400)

        session = StripeService.create_checkout_session(order, request.user)

        order.stripe_session_id = session.id
        order.save(update_fields=["stripe_session_id"])

        return Response({
            "checkout_url": session.url
        })
    