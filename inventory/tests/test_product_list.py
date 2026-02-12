from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor
from django.urls import reverse
from ..models import Category, Product


class TestProductListPublic(APITestCase):

    
    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email='vendor@test.com',
            password='password123',
            full_name='Test Vendor',
            business_name='Vendor Shop',
            tax_id='TAX-001'
        )
        self.category = Category.objects.create(name='Toys')

        self.product1 = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Toy Car',
            price=Decimal('15.99'),
            quantity=10,
            is_active=True,
            is_archived=False,
        )
        
        self.product2 = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Toy Ball',
            price=Decimal('5.99'),
            quantity=20,
            is_active=True,
            is_archived=False,
        )
        
        self.inactive_product = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Toy Hidden',
            price=Decimal('10.00'),
            quantity=5,
            is_active=False,
            is_archived=False,
        )

    def test_list_products_anonymous(self):
        url = reverse('inventory:product-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    
    def test_list_products_by_category_slug(self):


        books = Category.objects.create(name='Books')
        Product.objects.create(
            vendor=self.vendor,
            category=books,
            name='Python Book',
            price=Decimal('29.99'),
            quantity=5,
            is_active=True,
            is_archived=False,
        )
        

        url = reverse('inventory:product-list') + f'?category_slug={self.category.slug}'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

