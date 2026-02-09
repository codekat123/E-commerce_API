from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Client


class LogoutEndpointTests(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            full_name='Test User'
        )

    def test_logout_missing_refresh_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('users:logout'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Refresh token is required')

    def test_logout_invalid_refresh_token(self):
        self.client.force_authenticate(user=self.user)
        data = {'refresh': 'invalid_token'}
        response = self.client.post(reverse('users:logout'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid or expired refresh token')
