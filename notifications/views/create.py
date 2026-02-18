from rest_framework.generics import CreateAPIView
from ..serializers import NotificationCreateSerializer
from ..models import Notification
from users.permissions import IsAdmin , IsStaff


class CreateNotificationView(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = [IsAdmin | IsStaff]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)