from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Admin
from django.urls import reverse
from ..models import Category


class TestCategoryViewSet(APITestCase):

    def setUp(self):
        self.admin_user = Admin.objects.create_superuser(
            email='admin@test.com',
            password='adminpass',
            full_name='Admin User',
        )
        
        self.category = Category.objects.create(
            name='Home Appliances'
        )

    def test_category_slug_auto_generated(self):

        Category.objects.all().delete()
        cat = Category.objects.create(name='Electronics')
        
        self.assertIsNotNone(cat.slug)
        self.assertEqual(cat.slug, 'electronics')

    def test_category_unique_slug_handling(self):

        Category.objects.all().delete()
        cat1 = Category.objects.create(name='Books')
        cat2 = Category.objects.create(name='Books')
        

        self.assertNotEqual(cat1.slug, cat2.slug)
        self.assertEqual(Category.objects.count(), 2)
