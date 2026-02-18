from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from users.models.vendor import Vendor
from ..models import Product , Category


class TestSearch(APITestCase):

    def setUp(self):
        self.ventor = Vendor.objects.create_user(
            email="vendor@example.com",
            password="vendorpassword"
        )
        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(
            name="Smartphone",
            description="A powerful smartphone with a great camera.",
            price=699.99,
            category=self.category,
            vendor=self.ventor
        )

        self.product2 = Product.objects.create(
            name="Laptop",
            description="A high-performance laptop for work and gaming.",
            price=1299.99,
            category=self.category,
            vendor=self.ventor
        )

        self.product3 = Product.objects.create(
            name="Headphones",
            description="Noise-cancelling headphones with excellent sound quality.",
            price=199.99,
            category=self.category,
            vendor=self.ventor
        )
    
    def test_search(self):
        url = reverse('inventory:product-search') + f'?q={'Electronics'}'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
