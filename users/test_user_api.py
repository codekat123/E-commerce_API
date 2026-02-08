from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from users.models import Client, Staff, Admin


class UserAPITests(APITestCase):

    def test_register_success(self):
        url = reverse('users:register')
        payload = {
            'role': 'client',
            'full_name': 'Ahmed Gaber',
            'email': 'new.user@example.com',
            'password': 'strongpassword',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_role(self):
        url = reverse('users:register')
        payload = {
            'role': 'unknown',
            'full_name': 'Ahmed Gaber',
            'email': 'role.user@example.com',
            'password': 'strongpassword',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_full_name_validation(self):
        url = reverse('users:register')
        payload = {
            'role': 'client',
            'full_name': 'Ahmed',
            'email': 'name.user@example.com',
            'password': 'strongpassword',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        url = reverse('users:register')
        payload = {
            'role': 'client',
            'full_name': 'Ahmed Gaber',
            'email': 'short.pass@example.com',
            'password': 'short',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        # create an existing client
        Client.objects.create_user(
            email='dup@example.com', password='password123', full_name='Dup User'
        )
        url = reverse('users:register')
        payload = {
            'role': 'client',
            'full_name': 'Dup User',
            'email': 'dup@example.com',
            'password': 'anotherpassword',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_missing_refresh(self):
        url = reverse('users:logout')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_refresh(self):
        url = reverse('users:logout')
        response = self.client.post(url, {'refresh': 'invalidtoken'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_success_with_valid_refresh(self):
        email = 'admin.user@example.com'
        password = 'adminpassword'
        # create an admin user instance directly to avoid manager kwargs issues
        admin = Admin(email=email, full_name='Admin User')
        admin.set_password(password)
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.save()

        # obtain tokens
        token_url = reverse('users:login')
        resp = self.client.post(token_url, {'email': email, 'password': password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        refresh = resp.data.get('refresh')
        self.assertIsNotNone(refresh)

        logout_url = reverse('users:logout')
        resp2 = self.client.post(logout_url, {'refresh': refresh}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)

    def test_staff_create_permissions_and_success(self):
        url = reverse('users:staff_create')
        payload = {
            'email': 'staff1@example.com',
            'department': 'support',
            'employee_id': 'EMP001',
        }

        # unauthenticated -> 401
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticated non-admin -> 403
        Client.objects.create_user(email='c@example.com', password='pass12345', full_name='Client User')
        client_user = Client.objects.get(email='c@example.com')
        self.client.force_authenticate(user=client_user)
        resp2 = self.client.post(url, payload, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=None)

        # admin -> success
        admin = Admin(email='admin2@example.com', full_name='Admin Two')
        admin.set_password('adminpass')
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.save()
        self.client.force_authenticate(user=admin)
        resp3 = self.client.post(url, payload, format='json')
        self.assertEqual(resp3.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Staff.objects.filter(email=payload['email']).exists())
