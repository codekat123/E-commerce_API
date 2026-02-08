from celery import shared_task
from services.email import BrevoEmailService
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ..utils import build_user_link
from ..models import Staff
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def send_email_to_set_pasword(self,user_id):
    try:
        user = get_object_or_404(User,id=user_id)

        if not isinstance(user,Staff):
            raise ValueError('only one you can send set password email ')
    

        link = build_user_link(user,'users:staff_set_password')
        hmtl = render_to_string(
            "auth/set_password.html",
            {'user':user,'link':link}
        )
        BrevoEmailService().send(
            user.email,
            'please set your password to activate your email',
            hmtl
        )
    except Exception as e:
        logger.exception(
            'failed to send email',
            extra={'user_id':user_id}
        )