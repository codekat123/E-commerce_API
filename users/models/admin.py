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


    def save(self, *args, **kwargs):
        self.is_superuser = True
        self.is_staff = True
        super().save(*args, **kwargs)