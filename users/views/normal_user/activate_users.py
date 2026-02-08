from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from ...utils import get_user_from_token


class ActivateUser(View):
    def get(self, request, token, uuid):
        try:
            user = get_user_from_token(uuid, token)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("/")

        if user.is_active:
            messages.info(request, "Your account is already activated")
            return redirect("/")

        user.is_active = True
        user.save(update_fields=["is_active"])

        messages.success(
            request,
            "Your account has been activated successfully"
        )
        return redirect("/")
