from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Client, Vendor


class RegisterEndpointTests(APITestCase):

    def test_client_registration_success(self):
        data = {
            'role': 'client',
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_vendor_registration_success(self):
        data = {
            'role': 'vendor',
            'full_name': 'Jane Vendor',
            'email': 'vendor@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_invalid_role(self):
        data = {
            'role': 'superuser',
            'full_name': 'Hacker',
            'email': 'hacker@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'you can either register as customer or merchant')

    def test_duplicate_email(self):
        Client.objects.create_user(
            email='existing@example.com',
            password='testpass123',
            full_name='Existing User'
        )
        data = {
            'role': 'client',
            'full_name': 'Another User',
            'email': 'existing@example.com',
            'password': 'securepass123'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        data = {
            'role': 'client',
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'password': 'short'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_fields(self):
        data = {
            'role': 'client',
            'email': 'john@example.com'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
