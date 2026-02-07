from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

User = get_user_model()


class ActivateUser(View):
    def get(self, request, token, uuid):
        uid = force_str(urlsafe_base64_decode(uuid))
        user = get_object_or_404(User, pk=uid)

        if user.is_active:
            messages.info(request, "Your account is already activated")
            return redirect("/")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])

            messages.success(
                request,
                "Your account has been activated successfully "
            )
            return redirect("/")

        messages.error(request, "Invalid or expired activation link")
        return redirect("/")
