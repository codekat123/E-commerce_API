from django.db.models import TextChoices


class TransactionType(TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAW = "withdraw", "Withdraw"
    PAYMENT = "payment", "Payment"



class Status(TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"