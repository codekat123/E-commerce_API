from .base import BaseUserModel
from django.db import models
from django.core.validators import RegexValidator
from ..utils import get_country_choices


class Client(BaseUserModel):

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999.',
    )
    phone_number = models.CharField(
        'phone number',
        validators=[phone_regex],
        max_length=17,
        blank=True,
    )
    country = models.CharField(
        'country',
        choices=get_country_choices(),
        max_length=60,
        blank=True,
    )
    location = models.TextField(
        'location',
        max_length=400,
        blank=True,
    )

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        db_table = 'users_client'
