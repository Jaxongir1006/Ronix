from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields

class Country(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
    )

    video = models.FileField(upload_to='marketing/', verbose_name=_('Video'))

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed name"
    
    @property
    def media_url(self):
        return self.video.url if self.video else ''
    
class Content(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Desciption'))
    )

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"