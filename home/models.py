from django.db import models
from parler.models import TranslatableModel,TranslatedFields
from django.utils.translation import gettext_lazy as _

class HomeBanner(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title'), blank=True, null=True),
        subtitle = models.CharField(max_length=200, verbose_name=_('Subtitle'), blank=True, null=True)
    )

    image = models.ImageField(upload_to='banners/', verbose_name=_('Image'), blank=True, null=True)

    class Meta:
        verbose_name = 'Home Banner'
        verbose_name_plural = 'Home Banners'

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def imageURL(self):
        return self.image.url if self.image else ''
    
    class Meta:
        verbose_name = _("Home Banner")
        verbose_name_plural = _("Home Banners")

class CustomerReview(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Description'))
    )

    video = models.FileField(upload_to='reviews/', verbose_name=_('Video'))

    def str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    @property
    def videoURL(self):
        return self.video.url if self.video else ''