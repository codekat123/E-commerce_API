from .base import BaseUserModel
from django.db import models


class Admin(BaseUserModel):
    """
    Admin user model for platform administrators.
    Admins have superuser privileges and full platform access.
    """

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'
        db_table = 'users_admin'
        permissions = [
            ('can_manage_users', 'Can manage all users'),
            ('can_manage_platform', 'Can manage platform settings'),
            ('can_view_reports', 'Can view platform reports'),
        ]

    def save(self, *args, **kwargs):
        self.is_superuser = True
        self.is_staff = True
        super().save(*args, **kwargs)