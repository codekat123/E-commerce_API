from rest_framework import serializers


class BaseRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )

    def validate_email(self, value):
        model = self.Meta.model
        if model.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_full_name(self, value):
        if len(value.split()) < 2:
            raise serializers.ValidationError(
                "Please enter your full name (first + last)."
            )
        return value
    
    def create(self, validated_data):
        model = self.Meta.model
        user = model(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
