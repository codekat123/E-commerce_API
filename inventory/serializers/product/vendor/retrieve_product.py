from rest_framework import serializers 
from ...rating import ProductRatingSerializer
from ....models import Product 
from ...image import ProductImageSerializer


class ProductVendorRetrieveSerializer(serializers.ModelSerializer):
    rating = ProductRatingSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = (
            'uuid',
            'name',
            'price',
            'quantity',
            'is_archived',
            'is_active',
            'created_at',
            'updated_at',
            'rating',
            'images',
        )
        read_only_fields = fields