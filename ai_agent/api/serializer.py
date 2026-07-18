from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=10_000,
        trim_whitespace=True,
    )

    conversation_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )


class ChatResponseSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField()
    response = serializers.CharField()
