from rest_framework import serializers 
from ....models import Product 
from users.serializers import VendorRetrieveSerializer
from ...rating import ProductRatingSerializer

class ProductRetrieveSerializer(serializers.ModelSerializer):
    vendor = VendorRetrieveSerializer(read_only=True)
    stock_status = serializers.SerializerMethodField()
    rating = ProductRatingSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name','uuid','description','price','vendor','stock_status','rating']
        read_only_fields = fields
        
    def get_stock_status(self,obj):
        return (
            "this product is about to finish"
            if obj.is_low_stock
            else "in stock"
        )