from rest_framework import serializers
from users.models import Vendor
from ..models import Notification


class NotificationCreateSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all()
    )

    title = serializers.CharField(min_length=3, trim_whitespace=True)
    body = serializers.CharField(trim_whitespace=True)

    class Meta:
        model = Notification
        fields = ['title', 'body', 'receiver']
