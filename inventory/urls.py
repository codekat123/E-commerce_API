from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDestroyAPIView,
    ProductListAPIView,
    ProductVendorListAPIView,
    ProductRatingCreateAPIView,
    ProductRatingDeleteAPIView,
    ProductRatingListAPIView,
    ProductRatingUpdateAPIView,
    ProductRetrieveAPIView,
    ProductVendorRetrieveAPIView,
)

app_name = "inventory"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [


    path("product/create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("product/<uuid:uuid>/update/", ProductUpdateAPIView.as_view(), name="product-update"),
    path("product/<uuid:uuid>/delete/", ProductDestroyAPIView.as_view(), name="product-delete"),


    path("product/", ProductListAPIView.as_view(), name="product-list"),
    path("product/category/<slug:category_slug>/", ProductListAPIView.as_view(), name="product-category-list"),
    path("product/<uuid:uuid>/", ProductRetrieveAPIView.as_view(), name="product-retrieve"),


    path("product/vendor/", ProductVendorListAPIView.as_view(), name="product-vendor-list"),
    path("product/<uuid:uuid>/vendor/", ProductVendorRetrieveAPIView.as_view(), name="product-vendor-retrieve"),


    path("product/<uuid:uuid>/ratings/", ProductRatingListAPIView.as_view(), name="product-rating-list"),
    path("product/<uuid:uuid>/ratings/create/", ProductRatingCreateAPIView.as_view(), name="product-rating-create"),
    path("product/rating/<int:pk>/update/", ProductRatingUpdateAPIView.as_view(), name="product-rating-update"),
    path("product/rating/<int:pk>/delete/", ProductRatingDeleteAPIView.as_view(), name="product-rating-delete"),
]

urlpatterns += router.urls
