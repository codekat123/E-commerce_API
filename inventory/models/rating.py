from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Client
from .product import Product


class ProductRating(models.Model):
    customer = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="product_ratings"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    stars = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_ratings"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "product"],
                name="unique_customer_product_rating"
            )
        ]

    def __str__(self):
        return f"{self.stars} ⭐ - {self.product}"
