from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import Vendor
from wallet.models import Wallet


class TestMyWalletAPIView(APITestCase):

    def setUp(self):
        self.password = "StrongPassword123"

        self.vendor = Vendor.objects.create_user(
            email="vendor@example.com",
            password=self.password,
            tax_id="TAX-002"
        )

        self.wallet = Wallet.objects.create(
            user=self.vendor,
            balance=334.30
        )

        self.url = reverse("wallet:my-wallet")


    def test_authenticated_vendor_can_get_wallet(self):
        self.client.force_authenticate(user=self.vendor)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], "334.30")
        self.assertIn("transactions", response.data)
        self.assertEqual(len(response.data["transactions"]), 0)


    def test_unauthenticated_user_cannot_access_wallet(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

