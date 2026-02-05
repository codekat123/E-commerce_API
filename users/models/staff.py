from .base import BaseUserModel
from django.db import models


class Staff(BaseUserModel):

    DEPARTMENT_CHOICES = [
        ('support', 'Customer Support'),
        ('admin', 'Administration'),
        ('moderation', 'Content Moderation'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    department = models.CharField(
        'department',
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        default='other',
    )
    employee_id = models.CharField(
        'employee ID',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff members'
        db_table = 'users_staff'
        permissions = [
            ('can_moderate_content', 'Can moderate user content'),
            ('can_manage_vendors', 'Can manage vendors'),
            ('can_view_analytics', 'Can view platform analytics'),
        ]

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)