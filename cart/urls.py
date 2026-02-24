from django.urls import path
from .views import CartView, CartItemView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("items/", CartItemView.as_view(), name="cart-items"),
]