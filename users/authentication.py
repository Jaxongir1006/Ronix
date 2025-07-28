from django.contrib.auth.backends import BaseBackend
from .models import User
from django.core.cache import cache

class PasswordOrCodeBackend(BaseBackend):
    def authenticate(self, request, login_input=None, password=None, code=None, **kwargs):
        """
        Foydalanuvchini email yoki telefon raqam orqali topadi,
        va parol yoki SMS kod asosida autentifikatsiya qiladi.
        """
        user = None

        if not login_input:
            return None

        # Email va telefon raqam bir xil uzunlikda bo'lishi mumkin, shuning uchun ikkisini ham tekshiramiz
        user = User.objects.filter(phone_number=login_input).first() or \
               User.objects.filter(email=login_input).first()

        if not user:
            return None

        # Parol bilan autentifikatsiya
        if password and user.check_password(password):
            return user

        # SMS verification code bilan autentifikatsiya
        cached_code = cache.get(f"user_register_{user.email}")

        if not cached_code:
            return None

        if cached_code == code:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
