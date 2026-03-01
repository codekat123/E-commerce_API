from django.contrib import admin
from .models import Wallet, Transaction



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance', 'updated_at')
    search_fields = ('user__email',)
    ordering = ('-updated_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payment_uuid', 'wallet', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('wallet__user__email',)
    ordering = ('-created_at',)