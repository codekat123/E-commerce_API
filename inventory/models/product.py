import uuid
from django.db import models
from users.models import Vendor
from .category import Category

class Product(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    vendor = models.ForeignKey(
        Vendor,  
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,  
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    quantity = models.PositiveIntegerField(default=0)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_archived = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["vendor"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.vendor})"
    
    @property
    def is_low_stock(self):
        return self.quantity < 30
    

