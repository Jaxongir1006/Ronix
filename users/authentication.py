from django.contrib.auth.backends import BaseBackend
from .models import User

class CodeAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, code=None, **kwargs):
        try:
            user = User.objects.get(phone_number=username)
            if user.verification_code == code:
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
                if user.verification_code == code:
                    return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
