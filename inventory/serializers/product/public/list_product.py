from rest_framework import serializers
from ....models import Product
from ...image import ProductImageSerializer

class ProductListSerializer(serializers.ModelSerializer):

    avg_stars = serializers.FloatField(read_only=True)
    images = ProductImageSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = ('uuid','name','images','avg_stars')
        read_only_fields = fields
