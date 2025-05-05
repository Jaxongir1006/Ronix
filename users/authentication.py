from django.contrib.auth.backends import BaseBackend
from .models import User

class PasswordOrCodeBackend(BaseBackend):
    def authenticate(self, request, login_input=None, password=None, code=None, **kwargs):
        try:
            user = User.objects.get(phone_number=login_input)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=login_input)
            except User.DoesNotExist:
                return None

        # Avval parolni tekshiradi
        if password and user.check_password(password):
            return user

        # Agar parol yo'q bo'lsa, SMS kod orqali tekshiradi
        if code and user.verification_code == code:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
