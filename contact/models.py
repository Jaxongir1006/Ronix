from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactUs(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Full name'))
    phone = models.IntegerField(verbose_name=_('Phone number'))
    email = models.EmailField(verbose_name=_('Email address'))
    message = models.TextField(verbose_name=_('Message'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")
        ordering = ['-created_at']