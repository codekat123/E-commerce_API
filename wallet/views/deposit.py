from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ..serializer import DepositSerializer
from services import StripeService


class DepositAPIView(GenericAPIView):
    serializer_class = DepositSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = StripeService.create_deposit_session(
            amount=serializer.validated_data["amount"],
            user=request.user
        )

        return Response({
            "checkout_url": session.url
        })