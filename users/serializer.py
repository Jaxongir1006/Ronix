from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _
from core.utils import generate_verification_code, send_email_code,send_sms

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        
        email = validated_data.pop('email', None)
        phone_number = validated_data.pop('phone_number', None)

        code = generate_verification_code()

        user = User(
            email=email,
            phone_number=phone_number,
            verification_code=code,
            **validated_data
        )
        user.set_password(password)
        user.save()

        if email:
            send_email_code(email, code)
        elif phone_number:
            send_sms(phone_number, code)

        return user

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        if not attrs.get('phone_number') and not attrs.get('email'):
            raise serializers.ValidationError(_("Phone number or email is required."))
        return attrs


class LoginSerializer(serializers.Serializer):
    login_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login_input = data.get('login_input')
        password = data.get('password')

        user = User.objects.filter(email=login_input).first()
        if not user:
            user = User.objects.filter(phone_number=login_input).first()

        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Parol notogri.")

        if not user.is_verified:
            raise serializers.ValidationError("Avval ro'yxatni tasdiqlang (kod orqali).")

        return {'user': user}


class SendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Email yoki telefon raqami kerak.")
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        user = None
        if phone_number:
            user = User.objects.filter(phone_number=phone_number).first()
        else:
            user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi.")

        code = generate_verification_code()
        user.verification_code = code
        user.save()

        if phone_number:
            send_sms(phone_number, code)
        elif email:
            send_email_code(email, code)

        return user

class ConfirmResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    code = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, data):
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Email yoki telefon raqami kerak.")
        if data.get('new_password1') != data.get('new_password2'):
            raise serializers.ValidationError('Password do not match!!!')
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        code = validated_data.get('code')
        new_password1 = validated_data.get('new_password1')
        validated_data.get('new_password2')

        user = None
        if email:
            user = User.objects.filter(email=email).first()
        else:
            user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi.")

        if user.verification_code != code:
            raise serializers.ValidationError("Sms kod notogri.")

        user.set_password(new_password1)
        user.verification_code = None
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'is_verified']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address']
