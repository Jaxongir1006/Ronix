from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields,TranslatableManager


class Branch(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, verbose_name=_('Branch name'))
    )
    image = models.ImageField(upload_to='branches/', verbose_name=_('Branch image'), null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name=_('Branch address'))
    phone = models.CharField(max_length=20, verbose_name=_('Branch phone number'), blank=True,null=True)
    email = models.EmailField(max_length=200, verbose_name=_('Branch email'), blank=True,null=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Invalid branch name'
    
    def imageURL(self):
        return self.image.url if self.image else ''
    
    objects = TranslatableManager()

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")