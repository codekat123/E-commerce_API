from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ..serializer import WithdrawSerializer
from ..service import WalletService


class WithdrawAPIView(GenericAPIView):

    serializer_class = WithdrawSerializer


    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tx = WalletService.withdraw(
            user=request.user,
            amount=serializer.validated_data["amount"],
            stripe_account_id=serializer.validated_data["stripe_account_id"]
        )

        return Response({
            "transaction_id": tx.payment_uuid,
            "status": tx.status
        })