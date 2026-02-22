from rest_framework import serializers
from .item_retrieve import OrderItemSerializer
from ..models import Order



class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'address',
            'phone_number',
            'status',
            'total_price',
            'created_at',
            'items'
        ]
        read_only_fields = fields

    