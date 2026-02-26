from rest_framework.generics import RetrieveAPIView
from ..serializer import WalletSerializer
from ..models import Wallet
from django.shortcuts import get_object_or_404


class WalletRetrieve(RetrieveAPIView):
    serializer_class = WalletSerializer

    def get_object(self):
        return get_object_or_404(Wallet,user=self.request.user)