from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginAPITestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse("users:login")  

        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="StrongPass123"
        )

    def test_login_success(self):

        data = {
            "email": "test@gmail.com",
            "password": "StrongPass123"
        }

        response = self.client.post(self.login_url, data)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):

        data = {
            "email": "test@gmail.com",
            "password": "WrongPassword"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_non_existing_user(self):

        data = {
            "email": "notfound@gmail.com",
            "password": "StrongPass123"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields(self):
        data = {
            "email": "test@gmail.com"
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
