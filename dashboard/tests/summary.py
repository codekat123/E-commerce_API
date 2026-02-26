from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Vendor, Client
from inventory.models import Product, Category
from order.models import Order, OrderItem


class VendorSummaryViewTest(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email="vendor@test.com",
            password="test123"
        )

        self.client_user = Client.objects.create_user(
            email="client@test.com",
            password="test123"
        )

        self.category = Category.objects.create(name="electronics")

        self.url = reverse("dashboard:vendor-dashboard-summary")

    def test_vendor_summary_success(self):
        self.client.force_authenticate(user=self.vendor)

        product1 = Product.objects.create(
            name="Product 1",
            description="desc",
            price=Decimal("100.00"),
            quantity=10,
            vendor=self.vendor,
            category=self.category,
            is_archived=False
        )

        product2 = Product.objects.create(
            name="Product 2",
            description="desc",
            price=Decimal("200.00"),
            quantity=5,
            vendor=self.vendor,
            category=self.category,
            is_archived=True
        )

        order = Order.objects.create(
            customer=self.client_user,
            total_price=Decimal("0.00") 
        )

        OrderItem.objects.create(
            order=order,
            product=product1,
            quantity=2,
            product_price=Decimal("100.00")
        )

        OrderItem.objects.create(
            order=order,
            product=product1,
            quantity=1,
            product_price=Decimal("100.00")
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_products"], 2)
        self.assertEqual(response.data["active_products"], 1)
        self.assertEqual(response.data["archived_products"], 1)
        self.assertEqual(response.data["total_items_sold"], 3)
        self.assertEqual(
            Decimal(response.data["total_revenue"]),
            Decimal("300.00")
        )