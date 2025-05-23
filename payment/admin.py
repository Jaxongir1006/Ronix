from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_operator', 'state', 'perform_time', 'transaction_id','created_at')
    search_fields = ('transaction_id',)
    list_filter = ('state',)
    ordering = ('-created_at',)