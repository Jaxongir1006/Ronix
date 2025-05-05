from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'), unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), blank=True, null=True, unique=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False, verbose_name=_('Username'))

    USERNAME_FIELD = 'email'  # Auth email orqali bo'ladi
    REQUIRED_FIELDS = []  # Username va password kiritish shart emas

    objects = UserManager()

    def __str__(self):
        return self.username or self.phone_number
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")