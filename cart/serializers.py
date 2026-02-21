from rest_framework import serializers



class CartSerializer(serializers.Serializer):

    product_uuid = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1,default=1)