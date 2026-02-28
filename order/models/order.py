from django.db import models
from users.models import Client
from phonenumber_field.modelfields import PhoneNumberField


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    customer = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="orders",
        db_index=True,
    )

    address = models.TextField()

    phone_number = PhoneNumberField(db_index=True)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer}"