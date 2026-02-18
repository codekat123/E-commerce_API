from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product 
from notifications.tasks import send_product_review_notification

@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):

    if created:
        send_product_review_notification.delay(instance.pk)
