from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor
from django.urls import reverse
from ..models import Category, Product


class TestProductUpdateDelete(APITestCase):


    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email='vendor@test.com',
            password='vendorpass',
            full_name='Test Vendor',
            business_name='Vendor Shop',
            tax_id='TAX-001'
        )
        
        self.other_vendor = Vendor.objects.create_user(
            email='other@test.com',
            password='otherpass',
            full_name='Other Vendor',
            business_name='Other Shop',
            tax_id='TAX-002'
        )

        self.category = Category.objects.create(name='Books')

        self.product = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Django Book',
            price=Decimal('49.99'),
            quantity=100,
            is_active=True,
        )

    def test_update_product_success(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-update', kwargs={'uuid': self.product.uuid})
        
        payload = {
            'name': 'Advanced Django',
            'price': Decimal('59.99'),
        }
        
        response = self.client.patch(url, payload, format='json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Advanced Django')
        self.assertEqual(self.product.price, Decimal('59.99'))

    def test_update_product_forbidden_other_vendor(self):

        self.client.force_authenticate(self.other_vendor)
        url = reverse('inventory:product-update', kwargs={'uuid': self.product.uuid})
        
        payload = {'name': 'Hacked Name'}
        response = self.client.patch(url, payload, format='json')
        
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
    
    def test_update_quantity_not_allowed(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-update', kwargs={'uuid': self.product.uuid})
        
        payload = {'quantity': 50}
        response = self.client.patch(url, payload, format='json')
        
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete_product_success(self):

        self.client.force_authenticate(self.vendor)
        url = reverse('inventory:product-delete', kwargs={'uuid': self.product.uuid})
        
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Product.objects.filter(uuid=self.product.uuid).exists())

    def test_delete_product_forbidden_other_vendor(self):

        self.client.force_authenticate(self.other_vendor)
        url = reverse('inventory:product-delete', kwargs={'uuid': self.product.uuid})
        
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
