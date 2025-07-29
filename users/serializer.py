from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'access_token', 'refresh_token']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": _("Passwords do not match.")})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # JWT tokens
        refresh = RefreshToken.for_user(user)
        validated_data['access_token'] = str(refresh.access_token)
        validated_data['refresh_token'] = str(refresh)

        return validated_data


class LoginSerializer(serializers.Serializer):
    login_input = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        login_input = attrs.get("login_input")
        password = attrs.get("password")

        user = User.objects.filter(email=login_input).first() or \
               User.objects.filter(username=login_input).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({"error": _("Invalid credentials")})

        refresh = RefreshToken.for_user(user)
        attrs["access_token"] = str(refresh.access_token)
        attrs["refresh_token"] = str(refresh)

        return attrs
