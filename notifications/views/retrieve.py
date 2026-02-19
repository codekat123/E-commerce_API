from rest_framework.generics import RetrieveAPIView
from ..models import Notification
from ..serializers import NotificationRetrieveSerializer
from users.permissions import IsAdmin, IsStaff


class NotificationRetrieveView(RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationRetrieveSerializer
    permission_classes = [IsAdmin | IsStaff]
    lookup_field = "id"

    def get_object(self):
        obj = super().get_object()
        
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        
        return obj
