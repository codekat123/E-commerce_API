from django.db import models 
from users.models import BaseUserModel



class Wallet(models.Model):
    user = models.OneToOneField(
        BaseUserModel,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
          models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name="wallet_balance_non_negative"
            )
        ]