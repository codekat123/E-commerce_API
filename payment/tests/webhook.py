import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from order.models import Order
from users.models import Client as UserClient


class StripeWebhookIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("payment:stripe-webhook")

        
        self.user = UserClient.objects.create(
            full_name="testuser",
            email="test@test.com",
            password="testpass123"
        )

        
        self.order = Order.objects.create(
            status="pending",
            total_price=100,
            customer=self.user
        )

    @patch("payment.views.webhook.stripe.Webhook.construct_event")
    def test_checkout_completed(self, mock_construct_event):

        
        mock_construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "amount_total": 100,
                    "metadata": {
                        "order_id": str(self.order.id)
                    }
                }
            }
        }

        response = self.client.post(
            self.url,
            data=json.dumps({"dummy": "data"}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="fake_signature",
        )

        self.assertEqual(response.status_code, 200)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "paid")