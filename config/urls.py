from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls',namespace='users')),
    path('inventory/',include('inventory.urls',namespace='inventory')),
    path('notifications/',include('notifications.urls',namespace='notifications')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('order/',include('order.urls',namespace='order')),
    path('payment/',include('payment.urls',namespace='payment')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]
