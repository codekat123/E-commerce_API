from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Client, Vendor


class GetProfileEndpointTests(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email='client@example.com',
            password='testpass123',
            full_name='Test Client'
        )

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:get_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(reverse('users:get_profile'))
        # RetrieveAPIView returns 401 UNAUTHORIZED for unauthenticated requests
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateProfileEndpointTests(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email='client@example.com',
            password='testpass123',
            full_name='Test Client'
        )

    def test_update_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'full_name': 'Updated Name'}
        response = self.client.put(reverse('users:update_profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_unauthenticated(self):
        data = {'full_name': 'Updated Name'}
        response = self.client.put(reverse('users:update_profile'), data)
        # UpdateAPIView returns 401 UNAUTHORIZED for unauthenticated requests
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteProfileEndpointTests(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email='client@example.com',
            password='testpass123',
            full_name='Test Client'
        )

    def test_delete_profile_authenticated(self):
        user_id = self.user.id
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('users:self_delete'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=user_id).exists())

    def test_delete_profile_unauthenticated(self):
        response = self.client.delete(reverse('users:self_delete'))
        # DestroyAPIView returns 401 UNAUTHORIZED for unauthenticated requests (not 403)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
