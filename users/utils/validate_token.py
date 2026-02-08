from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def get_user_from_token(uuid: str, token: str):
    try:
        uid = int(urlsafe_base64_decode(uuid))
        user = User.objects.get(pk=uid)
    except (ValueError, TypeError, User.DoesNotExist):
        raise ValidationError("Invalid activation link")

    if not default_token_generator.check_token(user, token):
        raise ValidationError("Invalid or expired token")

    return user
