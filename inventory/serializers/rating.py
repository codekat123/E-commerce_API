from rest_framework import serializers 
from ..models import ProductRating
from decimal import Decimal


class ProductRatingSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(
        source='customer.email',
        read_only=True
    )

    class Meta:
        model = ProductRating
        fields = ('stars', 'comment', 'created_at', 'customer_email')
        read_only_fields = ['created_at']

    def validate_stars(self, value):
        if value % Decimal("0.5") != 0:
            raise serializers.ValidationError(
                "Stars must be in 0.5 increments."
            )
        return value