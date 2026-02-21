from django.urls import path
from .views import CartView, CartItemView, CheckoutView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("items/", CartItemView.as_view(), name="cart-items"),
    path("checkout/", CheckoutView.as_view(), name="cart-checkout"),
]