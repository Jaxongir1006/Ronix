from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields


class Series(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
        description = models.CharField(max_length=200, verbose_name=_('Description'))
    )

    image = models.ImageField(upload_to='series/', verbose_name=_('Image'))

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Unnamed name'
    
    @property
    def imageURL(self):
        return self.image.url if self.image else ''

class SeriesCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, verbose_name=_('Name')),
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Description'))
    )

    series = models.ForeignKey(Series, on_delete=models.CASCADE, verbose_name=_("Series"), related_name='seriescategories')
    image = models.ImageField(upload_to='series/', verbose_name=_('Image'), blank=True, null=True)
    video = models.FileField(upload_to='series/', verbose_name=_('Video'), null=True, blank=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def media_url(self):
        return self.image.url if self.image else (self.video.url if self.video else "")

class Subcategory(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title'), blank=True, null=True),
        description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    )

    category = models.ForeignKey(SeriesCategory, on_delete=models.CASCADE, verbose_name=_('Category'))
    image = models.ImageField(upload_to='series/', verbose_name=_('image'), blank=True, null=True)
    video = models.FileField(upload_to='series/', verbose_name=_('Video'), null=True, blank=True)
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def imageURL(self):
        return self.image.url if self.image else ''
    
