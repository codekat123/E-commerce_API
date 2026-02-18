from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'body', 'is_read', 'created_at','recipient')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'body', 'recipient__email')
    ordering = ('-created_at',)