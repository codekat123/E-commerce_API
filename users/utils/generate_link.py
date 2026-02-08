from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.urls import reverse



def build_user_link(user,view_name):
    token = default_token_generator.make_token(user)
    uuid = urlsafe_base64_encode(force_bytes(user.pk))

    return (
        f"{settings.FRONTEND_DOMAIN.rstrip('/')}"
        f"{reverse(view_name,kwargs={'token':token,'uuid':uuid})}"
    )