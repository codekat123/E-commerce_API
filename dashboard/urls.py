from django.urls import path
from .views import (
    activate_product,
    DeactivateProductView,
    
)


app_name = 'dashboard'


urlpatterns = [
    path('products/<uuid:uuid>/activate/', activate_product.ActivateProductView.as_view(), name='activate-product'),
    path('products/<uuid:uuid>/deactivate/', DeactivateProductView.as_view(), name='deactivate-product'),
]