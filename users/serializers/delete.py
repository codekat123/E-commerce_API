from rest_framework import serializers

class AccountDeletionSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)