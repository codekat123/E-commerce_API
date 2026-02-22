from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Client
from ..models import Order





class OrderRetrieveAPITest(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email="user@test.com",
            password="password123"
        )

        self.other_user = Client.objects.create_user(
            email="other@test.com",
            password="password123"
        )

        self.order = Order.objects.create(
            customer=self.user,
            total_price=100
        )

        self.other_order = Order.objects.create(
            customer=self.other_user,
            total_price=200
        )

        self.url = reverse("order:order-detail", kwargs={"id": self.order.id})
        self.other_url = reverse("order:order-detail", kwargs={"id": self.other_order.id})

    def test_user_can_retrieve_own_order(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.order.id)

    def test_user_cannot_retrieve_other_users_order(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.other_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_retrieve_order(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)