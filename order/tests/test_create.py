from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from users.models import Client, Vendor
from inventory.models import Product, Category
from ..models import Order, OrderItem


class OrderCreateAPITest(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email="client@test.com",
            password="testpass123"
        )

        category = Category.objects.create(
            name="Test Category"
        )

        vendor = Vendor.objects.create_user(
            email="vendor@test.com",
            password="testpass123"
        )

        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("100.00"),
            quantity=10,
            category=category,
            vendor=vendor
        )

        self.payload = {
            "address": "in front of some shop behind this street",
            "phone_number": "+201004968716",
        }

        self.url = reverse('order:order-create')
        self.client.force_authenticate(self.user)
  
    @patch("order.views.create.CartService.get_cart")
    def test_create_order_successfully(self, mock_get_cart):
        mock_get_cart.return_value = {
            str(self.product.uuid): {
                "name": self.product.name,
                "price": float(self.product.price),
                "quantity": 2,
            }
        }

        response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = Order.objects.first()
        item = OrderItem.objects.first()

        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.total_price, Decimal("200.00"))
        self.assertEqual(item.quantity, 2)

    @patch("order.views.create.CartService.get_cart")
    def test_not_enough_stock(self, mock_get_cart):
        mock_get_cart.return_value = {
            str(self.product.uuid): {
                "name": self.product.name,
                "price": float(self.product.price),
                "quantity": 5,
            }
        }

        self.product.quantity = 1
        self.product.save()

        response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_requires_authentication(self):
        self.client.logout()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)