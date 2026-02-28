from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock

User = get_user_model()


class WithdrawAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        self.url = reverse("wallet:withdraw")  

    @patch("wallet.service.WalletService.withdraw")
    def test_successful_withdraw(self, mock_withdraw):

        self.client.force_authenticate(user=self.user)

        mock_tx = MagicMock()
        mock_tx.payment_uuid = "uuid-123"
        mock_tx.status = "completed"
        mock_withdraw.return_value = mock_tx

        response = self.client.post(self.url, {"amount": 100})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["transaction_id"], "uuid-123")
        self.assertEqual(response.data["status"], "completed")

        mock_withdraw.assert_called_once_with(
            user=self.user,
            amount=100,
            stripe_account_id=self.user
        )