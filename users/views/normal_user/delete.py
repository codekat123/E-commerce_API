from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from wallet.models import Wallet
from ...serializers import AccountDeletionSerializer

class SelfDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        serializer = AccountDeletionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]

        if not password or not user.check_password(password):
            raise ValidationError("Invalid password.")

        wallet = Wallet.objects.filter(user=user).first()
        if wallet and wallet.balance != 0:
            raise ValidationError(
                "You still have funds in your wallet. Withdraw them first."
            )

        return user