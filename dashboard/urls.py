from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    activate_product,
    DeactivateProductView,
    ProductArchive,
    VendorSummaryView,
    
)

router = DefaultRouter()
router.register(r'products', ProductArchive, basename='product-archive')


app_name = 'dashboard'


urlpatterns = [
    path('products/<uuid:uuid>/activate/', activate_product.ActivateProductView.as_view(), name='activate-product'),
    path('products/<uuid:uuid>/deactivate/', DeactivateProductView.as_view(), name='deactivate-product'),
    path('dashboard/summary/', VendorSummaryView.as_view(), name='vendor-dashboard-summary'),
] + router.urls