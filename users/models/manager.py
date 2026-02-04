from django.contrib.auth.models import BaseUserManager
from polymorphic.managers import PolymorphicManager


class CustomUserManager(BaseUserManager, PolymorphicManager):
    """
    Custom manager for polymorphic user model.
    Provides methods for creating users with proper validation.
    """

    def create_user(self, email, password, full_name, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, full_name, **extra_fields)