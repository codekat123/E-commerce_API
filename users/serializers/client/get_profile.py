from rest_framework import serializers
from ...models import Client


class ClientRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "email",
            "full_name",
            "phone_number",
            "country",
            "location",
        )
        read_only_fields = fields

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Update is not allowed.")

    def create(self, validated_data):
        raise serializers.ValidationError("Creation is not allowed.")
