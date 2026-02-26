import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal
from users.models import BaseUserModel
from wallet.service import WalletService


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookDepositAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
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

            if session["payment_status"] == "paid":
                user_id = session["metadata"]["user_id"]
                stripe_id = session["payment_intent"]
                amount = Decimal(session["amount_total"]) / 100

                user = BaseUserModel.objects.get(id=user_id)

                WalletService.deposit(
                    user=user,
                    amount=amount,
                    stripe_id=stripe_id
                )

        return Response(status=200)