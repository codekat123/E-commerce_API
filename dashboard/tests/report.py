from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Vendor ,Client
from datetime import date




class VendorReportAPITestCase(APITestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create_user(
            email="vendor@test.com",
            password="test123",

        )

        self.customer = Client.objects.create_user(
            email="customer@test.com",
            password="test123",
        )

        self.url = reverse("dashboard:vendor-report")  


    def test_vendor_can_download_report(self):
        self.client.force_authenticate(user=self.vendor)

        response = self.client.get(self.url, {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment;", response["Content-Disposition"])

    def test_non_vendor_cannot_access_report(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.get(self.url, {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthenticated_user_cannot_access_report(self):
        response = self.client.get(self.url, {
            "start_date": "2026-01-01",
            "end_date": "2026-02-01"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_date_format_returns_400(self):
        self.client.force_authenticate(user=self.vendor)

        response = self.client.get(self.url, {
            "start_date": "invalid-date",
            "end_date": "2026-02-01"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_dates_returns_400(self):
        self.client.force_authenticate(user=self.vendor)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)