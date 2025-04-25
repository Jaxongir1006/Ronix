from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'), unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")