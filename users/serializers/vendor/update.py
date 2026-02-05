from rest_framework import serializers
from ...models import Vendor


class VendorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ["is_active", "created_at", "updated_at", "email",'verified','verified_at']
