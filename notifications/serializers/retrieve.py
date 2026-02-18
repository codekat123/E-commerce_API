from rest_framework import serializers
from ..models import Notification


class NotificationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'sender', 'receiver', 'created_at']
        read_only_fields = fields 