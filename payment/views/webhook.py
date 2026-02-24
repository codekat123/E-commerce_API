import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session["metadata"]["order_id"]

            try:
                order = Order.objects.get(id=order_id)
                order.status = "paid"
                order.save(update_fields=["status"])
            except Order.DoesNotExist:
                pass

        return Response(status=200)