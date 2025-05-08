from rest_framework import serializers
from .models import Cart,CartItem
from products.serializers import ProductForCartSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductForCartSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cart', 'product']
        read_only_fields = ['id', 'cart']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'cart_items']
