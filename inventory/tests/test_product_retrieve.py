from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Product , Category
from users.models import Vendor 

class TestProductRetrieve(APITestCase):

    def test_product_retrieve(self):
        vender = Vendor.objects.create_user(
            email='just_vendor@gmail.com',
            password='consider_this_as_strongest_password_ever'
        )
        category = Category.objects.create(name='hmmm_let_us_just_name_it_category_cool_right')
        product = Product.objects.create(
            name='just_product',
            description='bal-bal-bal',
            quantity=5,
            price=45,
            vendor=vender,
            category=category
        )

        url = reverse('inventory:product-retrieve',kwargs={'uuid':product.uuid})

        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['results']['uuid'],product.uuid)