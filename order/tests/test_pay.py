from rest_framework import status
from rest_framework.test import APITestCase
from order.models import Order
from django.urls import reverse
from users.models import Client
from wallet.models import Wallet



class PayOrderAPITestCase(APITestCase):

    def setUp(self):
        self.user = Client.objects.create(
            email='vendor@example.com',
            password='password123',
            )
        self.order = Order.objects.create(
            customer=self.user,
            total_price=100.00,
            address='123 Main St',
            phone_number='+1234567890',
        )
        Wallet.objects.filter(user=self.user).update(balance=200.00)
        self.client.force_authenticate(user=self.user)

    def test_pay_order(self):
        url = reverse('order:order-pay', kwargs={'id': self.order.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')