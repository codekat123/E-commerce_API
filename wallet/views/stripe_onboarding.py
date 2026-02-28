from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.stripe_connect import StripeConnectService


class StripeOnboardingAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        if not user.stripe_account_id:
            StripeConnectService.create_connect_account(user)

        url = StripeConnectService.create_onboarding_link(user)

        return Response({"onboarding_url": url})