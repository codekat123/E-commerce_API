from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor
from django.urls import reverse
from ..models import Category, Product


class TestProductVendorList(APITestCase):


    def setUp(self):
        self.vendor1 = Vendor.objects.create_user(
            email='vendor1@test.com',
            password='password123',
            full_name='Vendor One',
            business_name='Shop One',
            tax_id='TAX-V1'
        )
        
        self.vendor2 = Vendor.objects.create_user(
            email='vendor2@test.com',
            password='password123',
            full_name='Vendor Two',
            business_name='Shop Two',
            tax_id='TAX-V2'
        )

        self.category = Category.objects.create(name='Electronics')


        Product.objects.create(
            vendor=self.vendor1,
            category=self.category,
            name='Phone',
            price=Decimal('599.99'),
            quantity=10,
            is_active=True,
        )
        Product.objects.create(
            vendor=self.vendor1,
            category=self.category,
            name='Tablet',
            price=Decimal('399.99'),
            quantity=5,
            is_active=True,
        )

        Product.objects.create(
            vendor=self.vendor2,
            category=self.category,
            name='Headphones',
            price=Decimal('199.99'),
            quantity=20,
            is_active=True,
        )

    def test_vendor_list_only_own_products(self):
        self.client.force_authenticate(self.vendor1)
        url = reverse('inventory:product-vendor-list')
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        print(response.data)
        print("Vendor FK type:", Product._meta.get_field("vendor").related_model)
        
        results = data.get('results', [data] if isinstance(data, list) else [])
        product_names = [item.get('name') for item in results]
        
        self.assertIn('Phone', product_names)
        self.assertIn('Tablet', product_names)
        self.assertNotIn('Headphones', product_names)
    
    def test_vendor_list_ordered_by_created_at(self):

        self.client.force_authenticate(self.vendor1)
        url = reverse('inventory:product-vendor-list')
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        results = data.get('results', [data] if isinstance(data, list) else [])
        

        self.assertEqual(len(results), 2)
    
    def test_vendor_list_requires_authentication(self):
        url = reverse('inventory:product-vendor-list')
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
