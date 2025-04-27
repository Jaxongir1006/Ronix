from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields,TranslatableModel

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))
    
    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
    
class AboutUs(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=255, verbose_name=_("Title")),
        subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Subtitle")),
    )
    image = models.ImageField(upload_to='aboutus/', blank=True, null=True, verbose_name=_("Image"))
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"
    
    @property
    def imageURL(self):
        if self.image:
            return self.imageURL
        else:
            return ''
        
    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")