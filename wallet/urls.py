from django.urls import path
from .views import (
    WalletRetrieve,
    StripeWebhookDepositAPIView,
    DepositAPIView,
    WithdrawAPIView,
)


app_name = 'wallet'


urlpatterns = [
    path('get/', WalletRetrieve.as_view(), name='my-wallet'),
    path('deposit/', DepositAPIView.as_view(), name='deposit'),
    path('webhook/stripe/', StripeWebhookDepositAPIView.as_view(), name='stripe-webhook-deposit'),
    path('withdraw/', WithdrawAPIView.as_view(), name='withdraw'),
]