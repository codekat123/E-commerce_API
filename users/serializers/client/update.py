from rest_framework import serializers 
from ...models import Client
import phonenumbers
import pycountry

class ClientUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=False,
        style={"input_type": "password"}
    )

    class Meta:
        model = Client
        exclude = ["is_active", "created_at", "updated_at", "email"]

    def validate_country(self, value):
        try:
            country = pycountry.countries.search_fuzzy(value)
        except LookupError:
            raise serializers.ValidationError("Invalid country.")
        return country[0].name

    def validate_full_name(self, value):
        if len(value.split()) < 2:
            raise serializers.ValidationError(
                "Please enter your full name (first + last)."
            )
        return value

    def validate_phone_number(self, value):
        try:
            phone = phonenumbers.parse(value, "EG")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid Egyptian phone number.")

        if not phonenumbers.is_valid_number(phone):
            raise serializers.ValidationError("Invalid Egyptian phone number.")

        return phonenumbers.format_number(
            phone,
            phonenumbers.PhoneNumberFormat.E164
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
