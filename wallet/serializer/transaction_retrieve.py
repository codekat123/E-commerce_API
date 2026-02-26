from rest_framework import serializers
from ..models import Transaction


class TransactionRetrireveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transaction_uuid','transaction_type','amount','note','created_at']
        read_only_fields = fields