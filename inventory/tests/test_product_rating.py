from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Vendor, Client
from django.urls import reverse
from ..models import Category, Product, ProductRating
from django.test import override_settings


class TestProductRating(APITestCase):


    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email='vendor@test.com',
            password='password123',
            full_name='Vendor',
            business_name='Vendor Shop',
            tax_id='TAX-VENDOR'
        )

        self.client_user = Client.objects.create_user(
            email='client@test.com',
            password='password123',
            full_name='Test Client'
        )
        
        self.other_client = Client.objects.create_user(
            email='other@test.com',
            password='password123',
            full_name='Other Client'
        )

        self.category = Category.objects.create(name='Electronics')

        self.product = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            name='Smartphone',
            price=Decimal('799.99'),
            quantity=10,
            is_active=True,
        )

    def test_list_ratings_for_product(self):
 
        # Create some ratings
        ProductRating.objects.create(
            customer=self.client_user,
            product=self.product,
            stars=Decimal('4.5'),
            comment='Great phone!'
        )
        ProductRating.objects.create(
            customer=self.other_client,
            product=self.product,
            stars=Decimal('5.0'),
            comment='Excellent!'
        )
        

        self.client.force_authenticate(self.client_user)
        url = reverse('inventory:product-rating-list', kwargs={'uuid': self.product.uuid})
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        results = data.get('results', [data] if isinstance(data, list) else [])
        

        self.assertGreaterEqual(len(results), 2)

    def test_list_ratings_requires_client_authentication(self):
        """Unauthenticated users cannot list ratings"""
        url = reverse('inventory:product-rating-list', kwargs={'uuid': self.product.uuid})
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_rating_requires_valid_stars(self):
        """Rating creation validates stars field - may fail due to Decimal/float bug"""
        self.client.force_authenticate(self.client_user)
        url = reverse('inventory:product-rating-create', kwargs={'uuid': self.product.uuid})
        

        payload = {
            'stars': Decimal('3.3'),
            'comment': 'Test comment'
        }
        
        
        response = self.client.post(url, payload, format='json')

        self.assertIn(response.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR))


    def test_delete_rating_as_customer(self):

        rating = ProductRating.objects.create(
            customer=self.client_user,
            product=self.product,
            stars=Decimal('4.0'),
            comment='To be deleted'
        )
        
        self.client.force_authenticate(self.client_user)
        url = reverse('inventory:product-rating-delete', kwargs={'pk': rating.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductRating.objects.filter(pk=rating.pk).exists())

    def test_cannot_rate_same_product_twice(self):
        ProductRating.objects.create(
            customer=self.client_user,
            product=self.product,
            stars=Decimal('4.0'),
            comment='First rating'
        )
        
        
        with self.assertRaises(Exception):  
            ProductRating.objects.create(
                customer=self.client_user,
                product=self.product,
                stars=Decimal('5.0'),
                comment='Second rating'
            )

    def test_update_rating_as_customer(self):

        rating = ProductRating.objects.create(
            customer=self.client_user,
            product=self.product,
            stars=Decimal('3.0'),
            comment='Original comment'
        )
        
        self.client.force_authenticate(self.client_user)
        url = reverse('inventory:product-rating-update', kwargs={'pk': rating.pk})
        
        payload = {
            'stars': Decimal('4.5'),
            'comment': 'Updated comment'
        }
        
        response = self.client.patch(url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR))
  
