from rest_framework import serializers
from ....models import Product
from ...rating import ProductRatingSerializer
from ...image import ProductImageSerializer

class ProductVendorListSerializer(serializers.ModelSerializer):
    rating = ProductRatingSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('uuid','name','price','is_active','is_archived','created_at','updated_at','rating','images')
        read_only_fields = fields