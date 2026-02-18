from rest_framework.generics import ListAPIView
from ..serializers import NotificationListSerializer
from ..models import Notification , NotificationAudience
from users.permissions import IsAdmin , IsStaff


class ListNotificationView(ListAPIView):
    serializer_class = NotificationListSerializer
    permission_classes = [IsAdmin | IsStaff]
    
    def get_queryset(self):
        return (
            Notification.objects.filter(
                audience=NotificationAudience.MANAGEMENT
            )
            .order_by('-created_at','is_read')
        )