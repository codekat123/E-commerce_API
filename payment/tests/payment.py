from unittest.mock import patch
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import Client
from order.models import Order




class CreateCheckoutSessionTest(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            full_name="testuser",
            email="test@test.com",
            password="testpass123"
        )

        self.order = Order.objects.create(
            customer=self.user,
            total_price=100,
            status="pending"
        )

        self.url = reverse(
            "payment:create-checkout-session",
            args=[self.order.id]
        )

    @patch("payment.views.payment.StripeService.create_checkout_session")
    def test_create_checkout_session_success(self, mock_create_session):

        
        class FakeSession:
            id = "cs_test_123"
            url = "https://stripe.com/test-checkout"

        mock_create_session.return_value = FakeSession()

        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["checkout_url"], FakeSession.url)

        self.order.refresh_from_db()
        self.assertEqual(self.order.stripe_session_id, "cs_test_123")