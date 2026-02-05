from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor,Client,Staff




@receiver(post_save,sender=Client)
def send_email_to_client(sender,instance,created,**kwargs):
    pass
