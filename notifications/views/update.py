from rest_framework.generics import UpdateAPIView
from ..serializers import NotificationUpdateSerializer
from ..models import Notification
from users.permissions import IsAdmin , IsStaff


class NotificationUpdateView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationUpdateSerializer
    permission_classes = [IsAdmin | IsStaff]
    lookup_field = 'id'