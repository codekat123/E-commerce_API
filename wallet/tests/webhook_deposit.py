from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
from decimal import Decimal

from users.models import Vendor


class TestStripeWebhookDepositAPIView(APITestCase):

    def setUp(self):
        self.user = Vendor.objects.create_user(
            email="vendor@example.com",
            password="StrongPassword123",
            tax_id="TAX-100"
        )

        self.url = reverse("wallet:stripe-webhook-deposit")

    @patch("wallet.views.webhook_deposit.WalletService.deposit")
    @patch("wallet.views.webhook_deposit.stripe.Webhook.construct_event")
    def test_successful_paid_checkout_triggers_deposit(
        self,
        mock_construct_event,
        mock_deposit
    ):

        mock_construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "payment_status": "paid",
                    "metadata": {
                        "user_id": str(self.user.id)
                    },
                    "payment_intent": "pi_12345",
                    "amount_total": 10000
                }
            }
        }

        response = self.client.post(
            self.url,
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="fake_signature"
        )

        self.assertEqual(response.status_code, 200)

        mock_deposit.assert_called_once_with(
            user=self.user,
            amount=Decimal("100.00"),
            stripe_id="pi_12345"
        )