from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'), unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), blank=True, null=True, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False, verbose_name=_('Username'))

    USERNAME_FIELD = 'email'  # Auth email orqali bo'ladi
    REQUIRED_FIELDS = []  # Username va password kiritish shart emas

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone_number
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('User'))
    first_name = models.CharField(max_length=100, verbose_name=_('First name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last name'))
    company = models.CharField(max_length=100, verbose_name=_('Company'))
    region = models.CharField(max_length=100, verbose_name=_('Region'))
    street = models.CharField(max_length=200, verbose_name=_('Street'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    number_house = models.CharField(max_length=50, verbose_name=_('House number'))
    number_apartment = models.CharField(max_length=50, verbose_name=_('Apartment number'))
    index = models.CharField(max_length=20, verbose_name=_('Index'))