from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(verbose_name=_('Email address'), unique=True, blank=True, null=True)
    phone_number = models.IntegerField(verbose_name=_('Phone number'), null=True, blank=True)
    is_distributor = models.BooleanField(default=False, verbose_name=_('Is distributor ?'))

    objects = UserManager()

    def __str__(self):
        return self.email
    
class PromoCode(models.Model):
    user = models.ForeignKey(verbose_name=_("user"),to=User,on_delete=models.CASCADE)
    code = models.CharField(verbose_name=_("promo_code"), max_length=10)

