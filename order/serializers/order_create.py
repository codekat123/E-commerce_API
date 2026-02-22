from rest_framework import serializers
from ..models import Order , OrderStatus


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['address', 'phone_number']