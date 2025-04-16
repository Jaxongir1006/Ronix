from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'promocode']
    search_fields = ['user__username', 'status', 'promocode__code']
    list_filter = ['status', 'user']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'discount']
    search_fields = ['order__id', 'product__name']
    list_filter = ['product', 'order']
 
 
 