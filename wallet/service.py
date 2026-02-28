from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Wallet, Transaction , TransactionType , Status
import stripe

class WalletService:

    @staticmethod
    @transaction.atomic
    def deposit(user, amount: Decimal, stripe_id: str | None = None):
        if amount <= 0:
            raise ValidationError("Deposit amount must be greater than zero.")

        wallet = Wallet.objects.select_for_update().get(user=user)


        if stripe_id and Transaction.objects.filter(stripe_id=stripe_id).exists():
            return wallet

        wallet.balance += amount
        wallet.save(update_fields=["balance"])

        Transaction.objects.create(
            wallet=wallet,
            type=TransactionType.DEPOSIT,
            amount=amount,
            stripe_reference_id=stripe_id,
        )

        return wallet

    @staticmethod
    @transaction.atomic
    def withdraw(user, amount: Decimal):

        wallet = Wallet.objects.select_for_update().get(user=user)

        if wallet.balance < amount:
            raise ValidationError("Insufficient funds.")

        tx = Transaction.objects.create(
            wallet=wallet,
            transaction_type=TransactionType.WITHDRAW,
            amount=amount,
            status=Status.PENDING
        )

        try:
            payout = stripe.Payout.create(
                amount=int(amount * 100),
                currency="usd",
                stripe_account=user.stripe_account_id, 
            )

            tx.stripe_reference_id = payout.id
            tx.status = Status.COMPLETED

            wallet.balance -= amount
            wallet.save(update_fields=["balance"])

            tx.save()

        except Exception:
            tx.status = Status.FAILED
            tx.save()
            raise

        return tx

    @staticmethod
    @transaction.atomic
    def pay_order(user, order):
        wallet = Wallet.objects.select_for_update().get(user=user)

        if wallet.balance < order.total_price:
            raise ValidationError("Insufficient wallet balance.")

        wallet.balance -= order.total_price
        wallet.save(update_fields=["balance"])

        Transaction.objects.create(
            wallet=wallet,
            transaction_type=TransactionType.PAYMENT,
            amount=order.total_price,
        )

        order.status = "paid"
        order.save(update_fields=["status"])

        return wallet