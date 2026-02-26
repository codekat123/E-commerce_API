import uuid
from django.db import models
from django.db.models import Q
from .wallet import Wallet
from .transaction_type import TransactionType , Status

class Transaction(models.Model):



    payment_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stripe_reference_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True   
    )

    note = models.TextField(
        max_length=500,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="transaction_amount_positive"
            )
        ]

        indexes = [
            models.Index(fields=["wallet", "transaction_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["stripe_reference_id"]),
        ]

    def __str__(self):
        return f"{self.wallet.user} | {self.transaction_type} | {self.amount} | {self.status}"