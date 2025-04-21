from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields

class Country(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
    )
    flag = models.ImageField(upload_to='flags/', verbose_name=_('Flag'))
    languages = models.CharField(max_length=100, verbose_name=_('Languages'))
    continent = models.CharField(max_length=100, choices=[
        ('asia_pacific', 'Asia - Pacific'),
        ('europe', 'Europe'),
        ('south_america', 'South America'),
        ('africa', 'Africa'),
    ], verbose_name=_('Continent'))

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Unnamed country'

    
class Content(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Desciption'))
    )

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='contents', verbose_name=_('Country'))

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"