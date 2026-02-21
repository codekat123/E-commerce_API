from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from inventory.models import Product, Category
from users.models import Vendor, Client
from decimal import Decimal
from cart.service import CartService


class TestCart(APITestCase):

    def setUp(self):
        self.user = Client.objects.create_user(
            email="user@test.com",
            password="StrongPassword123"
        )
        self.client.force_authenticate(self.user)

        self.vendor = Vendor.objects.create(
            email="vendor@test.com",
            full_name="vendor",
            password="StrongPassword123"
        )

        self.category = Category.objects.create(name="category")

        self.product = Product.objects.create(
            name="Product",
            category=self.category,
            vendor=self.vendor,
            quantity=10,
            price=Decimal("100.00"),
        )


        CartService.clear_cart(self.user)



    def test_add_product(self):
        url = reverse("cart:cart-items")

        response = self.client.post(url, {
            "product_uuid": str(self.product.uuid),
            "quantity": 2
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_price"], 200.0)
        self.assertEqual(
            response.data["items"][str(self.product.uuid)]["quantity"],
            2
        )


    def test_update_product(self):
        add_url = reverse("cart:cart-items")

        
        self.client.post(add_url, {
            "product_uuid": str(self.product.uuid),
            "quantity": 2
        }, format="json")

        
        update_url = reverse("cart:cart-items")

        response = self.client.patch(update_url, {
            "product_uuid": str(self.product.uuid),
            "quantity": 5
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_price"], 500.0)
        self.assertEqual(
            response.data["items"][str(self.product.uuid)]["quantity"],
            5
        )



    def test_remove_product(self):
        add_url = reverse("cart:cart-items")

    
        self.client.post(add_url, {
            "product_uuid": str(self.product.uuid),
            "quantity": 2
        }, format="json")

        delete_url = reverse("cart:cart-items")

        response = self.client.delete(delete_url, {
            "product_uuid": str(self.product.uuid)
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], {})
        self.assertEqual(response.data["total_price"], 0.0)