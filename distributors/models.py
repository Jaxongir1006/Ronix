from django.db import models
from django.utils.translation import gettext_lazy as _

class Distributor(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Full name'))
    phone = models.IntegerField(verbose_name=_('Phone number'))
    country = models.CharField(max_length=200,verbose_name=_('Country'))
    email = models.EmailField(verbose_name=_('Email address'))
    company = models.CharField(max_length=200, verbose_name=_('Company'))
    occupation = models.CharField(max_length=200, verbose_name=_('Occupation'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active ?'))

    def __str__(self):
        return self.name

