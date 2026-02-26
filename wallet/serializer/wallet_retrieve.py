from rest_framework import serializers
from ..models import Wallet
from .transaction_retrieve import TransactionRetrireveSerializer


class WalletSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["balance", "updated_at", "transactions"]

    def get_transactions(self, obj):
        last_ten = obj.transactions.order_by("-created_at")[:10]
        return TransactionRetrireveSerializer(last_ten, many=True).data