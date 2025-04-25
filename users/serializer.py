from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True, 'allow_blank': True},
            'phone_number': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone_number')

        if not email and not phone:
            raise serializers.ValidationError(_("Email yoki telefon raqamdan hech bo'lmaganda bittasi kerak."))

        return attrs