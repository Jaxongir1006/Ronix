from rest_framework import serializers
from .models import Cart,CartItem
from products.serializers import ProductForCartSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductForCartSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cart', 'product_detail', 'total_price']
        read_only_fields = ['id', 'cart']
    def get_total_price(self, obj:CartItem):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, required=False)
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_items', 'id', 'user', 'session_id', 'username', 'address', 'email', 'total_price']

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    def get_address(self, obj):
        return obj.user.address if obj.user else None
    
    def get_total_price(self, obj):
        items = obj.items.all()
        return sum(item.product.price * item.quantity for item in items)
