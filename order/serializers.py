from rest_framework import serializers
from .models import Order,OrderItem
from django.contrib.auth import get_user_model
from users.models import PromoCode
from django.utils.crypto import get_random_string

User = get_user_model()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'discount']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    user_email = serializers.EmailField(write_only=True, required=True)
    phone_number = serializers.IntegerField(write_only=True, required=False)
    promocode = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = ['status', 'user_email', 'phone_number', 'promocode', 'items']

    def create(self, validated_data):
        email = validated_data.pop('user_email')
        phone = validated_data.pop('phone_number', None)
        promo_code = validated_data.pop('promocode')
        items_data = validated_data.pop('items')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'phone_number': phone,
                'username': email,
                'password': get_random_string(8),
            }
        )

        if created:
            print("New user created")

        try:
            promocode_obj = PromoCode.objects.get(code=promo_code, user=user)
        except PromoCode.DoesNotExist:
            raise serializers.ValidationError("Promocode not found or not valid for this user.")

        order = Order.objects.create(user=user, promocode=promocode_obj, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order