from rest_framework.test import APITestCase 
from django.urls import reverse 
from inventory.models import Product , Category
from users.models import Vendor , Staff
from rest_framework import status


class TestActivateProduct(APITestCase):

    def setUp(self):

        category = Category.objects.create(name='just_category')
        vendor = Vendor.objects.create(
            email='test@example.com',
            password='strong_password'
        )

        self.product1 = Product.objects.create(
            name='laptop',
            description='it has ram and screen',
            price=393.3,
            quantity=34,
            vendor=vendor,
            category=category,
        )
        self.product2 = Product.objects.create(
            name='tablet',
            description='.. ....  ... ',
            price=393.3,
            quantity=34,
            vendor=vendor,
            category=category,
            is_active=True
        )
        staff = Staff.objects.create(
            email='ahmed@gmail.com',
            password='strong_password'
        )
        self.client.force_authenticate(staff)
        
    def test_activate_product(self):
        
        url = reverse('dashboard:activate-product',kwargs={'uuid':self.product1.uuid})

        response = self.client.post(url)

        self.assertEqual(status.HTTP_200_OK,response.status_code)
        
        self.product1.refresh_from_db()
        self.assertTrue(self.product1.is_active)
    
    def test_deactivate_product(self):
        url = reverse('dashboard:deactivate-product',kwargs={'uuid':self.product2.uuid})

        response = self.client.post(url)

        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.product2.refresh_from_db()
        self.assertFalse(self.product2.is_active)

