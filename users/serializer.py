from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

class RegisterLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        if not attrs.get('phone_number') and not attrs.get('email'):
            raise serializers.ValidationError(_("Phone number or email is required."))
        return attrs

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        if not attrs.get('phone_number') and not attrs.get('email'):
            raise serializers.ValidationError(_("Phone number or email is required."))
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'is_verified']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'username']