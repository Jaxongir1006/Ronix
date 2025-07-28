from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'), unique=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), unique=True)
    username = models.CharField(max_length=150, unique=False, verbose_name=_('Username'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone_number
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    