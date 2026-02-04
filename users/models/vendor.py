from .base import BaseUserModel
from django.db import models
from django.core.validators import MinLengthValidator


class Vendor(BaseUserModel):
    """
    Vendor user model for sellers/businesses.
    Stores vendor-specific information and business details.
    """

    business_name = models.CharField(
        'business name',
        max_length=150,
        validators=[MinLengthValidator(2)],
    )
    logo = models.ImageField(
        'business logo',
        upload_to='vendor_logos/%Y/%m/',
        null=True,
        blank=True,
    )
    verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Designates whether this vendor has been verified by admin.',
    )
    verified_at = models.DateTimeField(
        'verification date',
        null=True,
        blank=True,
    )
    tax_id = models.CharField(
        'tax ID',
        max_length=60,
        unique=True,
    )
    class Meta:
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'
        db_table = 'users_vendor'
        indexes = [
            models.Index(fields=['verified', 'is_active']),
        ]