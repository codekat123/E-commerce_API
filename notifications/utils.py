from .models import (
    Notification,
    NotificationAudience
)
from users.models import Staff , Vendor


def get_notification_management():
    return (
        Notification.objects
        .create(
            title='I\'m warning you for second time',
            body='I said if you send this product again I will destory your account here',
            audience=NotificationAudience.MANAGEMENT
        )
    )

def get_notification_for_vendors():
    return (
        Notification.objects
        .create(
            title='test',
            body='nothing to say just making sure you are still alive',
            audience=NotificationAudience.VENDOR
        )
    )


def get_staff():
    return (
        Staff.objects
        .create(full_name='Ahmed Gaber',email='ahmed@gmail.com',password='consider_this_strongerest_password_ever')
    )

def get_vendor():
    return (
        Vendor.objects
        .create(
            full_name='Ahmed Gaber',email='vendor@gmail.com',password='consider_this_strongerst_password_ever'
        )
    )




def create_dummy_notifications(count=10):
    notifications = [
        Notification(title="nothing", body="nothing",audience=NotificationAudience.MANAGEMENT)
        for _ in range(count)
    ]
    return Notification.objects.bulk_create(notifications)
