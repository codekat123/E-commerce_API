from rest_framework.generics import DestroyAPIView
from ..models import Notification , NotificationAudience
from users.models import Staff , Admin
from django.db.models import Q

class NotificationDestroyAPIView(DestroyAPIView):
    
    queryset = Notification.objects.all()

    def get_queryset(self):

        if isinstance(self.request.user,(Staff,Admin)):
            return Notification.objects.filter(
                audience=NotificationAudience.MANAGEMENT
            )
        else:
            return Notification.objects.filter(
            Q(sender=self.request.user) | 
            Q(recipient=self.request.user)
            )