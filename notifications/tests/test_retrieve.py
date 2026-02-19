from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 
from ..utils import (
    get_staff,
    get_notification_management
)


class TestRetrieveNotification(APITestCase):

    def setUp(self):
        self.notification = get_notification_management()
        self.url = reverse(
            "notifications:retrieve-notification",
            kwargs={"id": self.notification.pk}
        )
        self.staff = get_staff()
        self.client.force_authenticate(user=self.staff)

    def test_retrieve_returns_notification(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.notification.pk)
