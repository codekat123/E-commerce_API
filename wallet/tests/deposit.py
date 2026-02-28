from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from decimal import Decimal
from users.models import Vendor


class TestDepositAPIView(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email="vendor@example.com",
            password="StrongPassword123",
            tax_id="TAX-001"
        )

        self.url = reverse("wallet:deposit")

    @patch("wallet.views.deposit.StripeService.create_deposit_session")
    def test_deposit_creates_checkout_session(self, mock_create_session):
         
        mock_session = MagicMock()
        mock_session.url = "https://stripe.com/fake-session"
        mock_create_session.return_value = mock_session

        self.client.force_authenticate(user=self.vendor)

        response = self.client.post(self.url, {
            "amount": "100.00"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("checkout_url", response.data)
        self.assertEqual(
            response.data["checkout_url"],
            "https://stripe.com/fake-session"
        )

        mock_create_session.assert_called_once_with(
           amount=Decimal("100.00"),
            user=self.vendor
        )