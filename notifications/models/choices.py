from django.db.models import TextChoices



class NotificationAudience(TextChoices):
    ADMIN = "admin", "Admin"
    STAFF = "staff", "Staff"
    MANAGEMENT = "management", "Management"
    VENDOR = "vendor", "Vendor"
    CLIENT = "client", "Client"
