from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from services.email import BrevoEmailService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def send_verification_email(self, user_id):
    User = get_user_model()
    user = User.objects.filter(id=user_id).first()

    if not user:
        return

    if hasattr(user, "vendor") or hasattr(user, "staff"):
        raise ValueError("Cannot send verification email to staff or vendor")

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    link = f"{settings.FRONTEND_DOMAIN.rstrip('/')}{reverse('activation_user', kwargs={'token': token, 'uuid': uid})}"

    html = render_to_string(
        "auth/verification_email.html",
        {"user": user, "link": link}
    )

    BrevoEmailService().send(
        to_email=user.email,
        subject="Please verify your email address",
        html=html,
    )
