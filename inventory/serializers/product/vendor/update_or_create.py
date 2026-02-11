from rest_framework import serializers
from ....models import Product , Category , ProductImage
from ...image import ProductImageSerializer


class ProductVendorUpdateCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    images = ProductImageSerializer(many=True,write_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'quantity',
            'category',
            'images',
        )



    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Quantity cannot be negative."
            )
        return value

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "Product name must be at least 3 characters long."
            )
        return value



    def validate(self, attrs):

        if self.instance and 'quantity' in attrs:
            raise serializers.ValidationError({
                'quantity': 'Quantity cannot be updated after product creation.'
            })

        return attrs
    
    def create(self, validated_data):
        image_data = validated_data.pop('images')
        product  = Product.objects.create(**validated_data)

        for image in image_data:
            ProductImage.objects.create(product=product,**image_data)

        return product 