from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..utils import create_dummy_notifications , get_staff



class TestListNotification(APITestCase):

    def setUp(self):
        self.url = reverse("notifications:list-notifications")
        self.notifications = create_dummy_notifications(count=10)
        self.staff = get_staff()
        self.client.force_authenticate(user=self.staff)

    def test_list_returns_all_notifications(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

