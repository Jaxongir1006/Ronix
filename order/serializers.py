from rest_framework import serializers
from .models import Order,OrderItem
from django.utils.crypto import get_random_string
from core.utils import send_sms, send_email_code, generate_verification_code
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.utils.translation import gettext_lazy as _


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'discount']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    user_email = serializers.EmailField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['user_email', 'phone_number', 'items']

    def create(self, validated_data):
        email = validated_data.pop('user_email', None)
        phone = validated_data.pop('phone_number', None)
        items_data = validated_data.pop('items')

        if not email and not phone:
            raise serializers.ValidationError(_("Phone number or email is required."))

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'phone_number': phone,
                'username': email,
                'password': get_random_string(8),
            }
        )

        if not user.is_verified:
            code = generate_verification_code()
            user.verification_code = code
            user.save()

            if email:
                send_email_code(email, code)
                return {
                    "message": _("A verification code has been sent to your email."),
                    "email": email,
                    "status": False
                }
            elif phone:
                send_sms(phone, code)
                return {
                    "message": _("A verification code has been sent to your phone."),
                    "phone": phone,
                    "status": False
                }

        # User tasdiqlangan => order va order items yaratiladi
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order    


class OrderVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with this email does not exist."))

        if user.verification_code != code:
            raise serializers.ValidationError(_("Invalid verification code."))

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']

        user.is_verified = True
        user.verification_code = None
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items'] 