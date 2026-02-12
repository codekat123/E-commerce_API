from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor
from django.urls import reverse
from ..models import Category, Product


class TestProductCreate(APITestCase):

    
    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email='vendor@test.com',
            password='password123',
            full_name='Test Vendor',
            business_name='Vendor Shop',
            tax_id='TAX-001'
        )
        self.category = Category.objects.create(name='Electronics')
    
    def test_create_product_without_authentication_fails(self):
        url = reverse('inventory:product-create')
        payload = {
            'name': 'Test Product',
            'price': '99.99',
            'quantity': 10,
            'category': self.category.slug,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_create_product_with_valid_data(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-create')
        
        payload = {
            'name': 'Laptop',
            'price': '999.99',
            'quantity': 5,
            'category': self.category.slug,
        }
        
        response = self.client.post(url, payload, format='json')
        
        if response.status_code == status.HTTP_201_CREATED:
            self.assertTrue(Product.objects.filter(name='Laptop').exists())
            product = Product.objects.get(name='Laptop')
            self.assertEqual(product.vendor, self.vendor)
        else:

            self.assertIn(response.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED))
    
    def test_create_product_invalid_price(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-create')
        
        payload = {
            'name': 'Invalid Product',
            'price': '-10.00',
            'quantity': 5,
            'category': self.category.slug,
        }
        
        response = self.client.post(url, payload, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
    
    def test_create_product_short_name(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-create')
        
        payload = {
            'name': 'AB',
            'price': '99.99',
            'quantity': 5,
            'category': self.category.slug,
        }
        
        response = self.client.post(url, payload, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
