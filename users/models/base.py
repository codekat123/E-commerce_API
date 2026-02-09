from django.db import models
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)
from .manager import CustomUserManager


class BaseUserModel(AbstractBaseUser, PermissionsMixin, PolymorphicModel):
    
    email = models.EmailField(
        'email address',
        unique=True,
        db_index=True,
        max_length=100,
    )
    full_name = models.CharField(
        'full name',
        max_length=100,
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text='Designates whether this user should be treated as active.',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    created_at = models.DateTimeField(
        'date joined',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'date updated',
        auto_now=True,
    )
    groups = models.ManyToManyField(
        Group,
        related_name='user_set_custom',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def clean(self):
        super().clean()
        if len(self.full_name.strip()) < 2:
            raise ValidationError({'full_name': 'Full name must be at least 2 characters.'})