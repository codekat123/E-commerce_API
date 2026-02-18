from django.db import models
from django.contrib.auth import get_user_model
from .choices import NotificationAudience


User = get_user_model()

class Notification(models.Model):
    
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    audience = models.CharField(
    max_length=50,
    choices=NotificationAudience.choices)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'created_at']),
        ]