from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def with_email(self):
        return self.exclude(email__isnull=True).exclude(email__exact="")

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """Oddiy foydalanuvchini yaratish"""
        if not email and not phone_number:
            raise ValueError(_("Foydalanuvchida kamida email yoki telefon raqam bo'lishi kerak"))

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Superuser yaratish — bunda email majburiy"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError(_("Superuser yaratish uchun email bo'lishi kerak"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser uchun is_staff=True bo'lishi kerak"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser uchun is_superuser=True bo'lishi kerak"))

        return self.create_user(email=email, password=password, **extra_fields)
