from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields

class Country(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
    )

    video = models.FileField()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed name"
class Content(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Desciption'))
    )

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"