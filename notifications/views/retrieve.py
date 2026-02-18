from rest_framework.generics import CreateAPIView
from ..serializers import NotificationRetrieveSerializer
from ..models import Notification
from users.permissions import IsAdmin , IsStaff

class NotificationRetrieveView(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationRetrieveSerializer
    permission_classes = [IsAdmin | IsStaff]
    lookup_field = 'id'
