from rest_framework import serializers
from ...models import Vendor


class VendorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "email",
            "full_name",
            "logo",
            "verified",
            "tax_id",
        )
        read_only_fields = fields

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Update is not allowed.")

    def create(self, validated_data):
        raise serializers.ValidationError("Creation is not allowed.")
