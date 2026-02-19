from rest_framework import serializers
from ..models import Notification


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'body']
        read_only_fields = ['id', 'sender', 'created_at','recipient']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            if not request.user.is_staff or not request.user.is_superuser:
                raise serializers.ValidationError("You do not have permission to update this notification.")
        return super().validate(attrs)
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    def validate_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Body cannot be empty.")
        return value