import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from services.email import BrevoEmailService
from ..utils import build_user_link
from ..models import Staff, Admin

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def send_verification_email(self, user_id):
    try:
        User = get_user_model()
        user = User.objects.filter(id=user_id).first()

        if not user or isinstance(user, (Admin, Staff)):
            return

        link = build_user_link(user, "users:activate")

        html = render_to_string(
            "auth/verification_email.html",
            {"user": user, "link": link},
        )

        BrevoEmailService().send(
            to_email=user.email,
            subject="Please verify your email address",
            html=html,
        )

    except Exception:
        logger.exception(
            "Failed to send verification email",
            extra={"user_id": user_id},
        )
        raise