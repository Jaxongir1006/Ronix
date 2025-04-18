from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy as _

class HomeBanner(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        subtitle = models.CharField(max_length=200, verbose_name=_('Subtitle'))
    )

    image = models.ImageField(upload_to='banners/', verbose_name=_('Image'))

    class Meta:
        verbose_name = 'Home Banner'
        verbose_name_plural = 'Home Banners'

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def imageURL(self):
        return self.image.url if self.image else ''
    
class CustomerReview(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Description'))
    )

    video = models.FileField(upload_to='customer_review/')

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def videoURL(self):
        return self.video.url if self.video else ''

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

