from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'))
    phone_number = models.IntegerField(verbose_name=_('Phone number'))
    is_distributor = models.BooleanField(default=False, verbose_name=_('Is distributor ?'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email