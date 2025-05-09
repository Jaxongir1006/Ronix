from rest_framework import serializers
from .models import Order,OrderItem
from django.utils.crypto import get_random_string
from core.utils import send_sms, send_email_code, generate_verification_code
from users.models import User
from django.utils.translation import gettext_lazy as _

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)
    user_email = serializers.EmailField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['user_email', 'phone_number', 'items']

    def validate(self, attrs):
        if not attrs.get('user_email') and not attrs.get('phone_number'):
            raise serializers.ValidationError(_("Phone number or email is required."))
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('user_email', None)
        phone = validated_data.pop('phone_number', None)
        items_data = validated_data.pop('items')

        user = self._get_or_create_user(email, phone)

        if not user.is_verified:
            self._send_verification(user, email, phone)
            raise serializers.ValidationError(
                _("Verification code sent. Please verify your account before ordering.")
            )

        return self._create_order(user, items_data, validated_data)

    def _get_or_create_user(self, email, phone):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'phone_number': phone,
                'username': email or phone,
                'password': get_random_string(8),
            }
        )
        return user

    def _send_verification(self, user, email, phone):
        code = generate_verification_code()
        user.verification_code = code
        user.save()

        if email:
            send_email_code(email, code)
        elif phone:
            send_sms(phone, code)

    def _create_order(self, user, items_data, extra_data):
        order = Order.objects.create(user=user, **extra_data)

        order_items = [
            OrderItem(order=order, **item_data) for item_data in items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'created_at', 'items']