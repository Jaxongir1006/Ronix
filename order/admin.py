from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    search_fields = ['user__username', 'status']
    list_filter = ['status', 'user']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']
    list_filter = ['product', 'order']
 
 
 