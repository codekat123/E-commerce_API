from django.urls import path

from .views import (
    StripeWebhookAPIView,
    CreateCheckoutSessionAPIView,
)

app_name = 'payment'


urlpatterns = [
    path("stripe/webhook/", StripeWebhookAPIView.as_view(), name="stripe-webhook"),
    path("orders/<int:order_id>/pay/", CreateCheckoutSessionAPIView.as_view(), name="create-checkout-session"),
]