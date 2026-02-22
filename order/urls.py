from django.urls import path
from .views import (
    OrderCreateAPIView,
    OrderRetrieveAPIView,
    OrderDestroyAPIView
)

app_name = 'order'


urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('<int:id>/', OrderRetrieveAPIView.as_view(), name='order-detail'),
    path('<int:id>/delete/', OrderDestroyAPIView.as_view(), name='order-delete'),

]