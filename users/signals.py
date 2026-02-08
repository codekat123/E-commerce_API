from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_verification_email , send_email_to_set_pasword
from .models import (
    BaseUserModel,
    Client,
    Vendor,

)


@receiver(post_save,sender=BaseUserModel)
def send_email_to_client(sender,instance,created,**kwargs):
    if not created:
        return
    
    
    if isinstance(instance,Client) or isinstance(instance,Vendor):
        send_verification_email(instance.pk)
    else:
        send_email_to_set_pasword(instance.pk)
