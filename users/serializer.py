from rest_framework import serializers
from .models import User,Address
from django.utils.translation import gettext_lazy as _
from core.utils import send_email_code,generate_verification_code
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'username', 'password1', 'password2']

    def validate(self, attrs):        
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})

        return attrs
   
    def create(self, validated_data):
        validated_data.pop('password2')
        code = generate_verification_code()
        user_data = {
            'phone_number': validated_data['phone_number'],
            'email': validated_data['email'],
            'username': validated_data['username'],
            'password1': validated_data['password1'],
            'code':code,
        }
        cache.set(f"user_register_{validated_data['email']}", user_data, timeout=120)

        send_email_code(validated_data['email'], code)

        return user_data
    
class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get("code")

        cached_things = cache.get(f"user_register_{email}")
        if not cached_things:
            raise serializers.ValidationError({"error": _("Verification data not found or expired.")})

        cache_code = cached_things['code']

        if not cache_code:
            raise serializers.ValidationError({"error": _("Verification code not set")})

        if cache_code != code:
            raise serializers.ValidationError({"error": _("Invalid verification code")})
        
        password = cached_things.pop("password1")
        cached_things.pop("code")
        user = User(**cached_things)
        user.set_password(password)
        user.save()

        # Kodni Redisdan o'chirish
        cache.delete(f"user_register_{email}")

        token = RefreshToken.for_user(user)
        attrs["access_token"] = str(token.access_token)
        attrs["refresh_token"] = str(token)

        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number']

class LoginSerializer(serializers.Serializer):
    login_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login_input = attrs.get("login_input")
        password = attrs.get("password")

        user = User.objects.filter(email=login_input).first() or \
               User.objects.filter(phone_number=login_input).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({"error": _("Invalid credentials")})

        # JWT tokenlar
        token = RefreshToken.for_user(user)
        attrs["access_token"] = str(token.access_token)
        attrs["refresh_token"] = str(token)
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication credentials were not provided.")

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": _("Old password is incorrect")})

        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": _("New passwords didn't match")})

        return attrs    

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()

class ChangePasswordWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({"error": _("User with this email does not exist")})

        # Generate and send verification code
        code = generate_verification_code()
        cache.set(f"user_code_{user.id}", code, timeout=120)
        send_email_code(user.email, code)

        return attrs
    
class VerifyCodeChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        code = attrs.get("code")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        cached_code = cache.get(f"user_code_{user_id}")

        if not cached_code:
            return serializers.ValidationError({"error": _("Verification code not set")})
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": _("User not found")})

        if cached_code != code:
            raise serializers.ValidationError({"error": _("Invalid verification code")})

        if password1 != password2:
            raise serializers.ValidationError({"error": _("Passwords didn't match")})

        user.set_password(password1)
        user.save()

        return attrs
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'username', 'first_name', 'last_name']

    def update(self, instance:User, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance
    
class UserEmailVerifySerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user

        cached_code = cache.get(f"user_code_{user.id}")

        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication credentials were not provided.")

        if not cached_code:
            raise serializers.ValidationError({"error": _("Verification code not set")})

        if cached_code != attrs['code']:
            raise serializers.ValidationError({"error": _("Invalid verification code")})

        cache.delete(user.id)

        return attrs
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'first_name', 'last_name', 'company', 'region', 'street', 'city', 'number_house', 'number_apartment', 'index']
        read_only_fields = ['id']

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)
        return address

    def update(self, instance, validated_data):        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        cached_data = cache.get(f"user_register_{email}")
        if not cached_data:
            raise serializers.ValidationError({"error": _("User data not found or expired. Please register again.")})

        # Yangi kod generatsiya qilinadi
        new_code = generate_verification_code()
        cached_data["code"] = new_code
        cache.set(f"user_register_{email}", cached_data, timeout=120)

        # Kod yuboriladi
        send_email_code(email, new_code)

        return {"email": email}