from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Staff , Vendor
from ..utils import get_staff , get_vendor


class TestCreateNotification(APITestCase):

    def setUp(self):
        self.url = reverse("notifications:create-notification")
        self.staff = get_staff()
        self.vendor = get_vendor()
        self.client.force_authenticate(user=self.staff)

    def test_create_notification(self):
        payload = {
            "title": "just_title",
            "body": "nothing_fancy",
            "recipient": self.vendor.pk,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
