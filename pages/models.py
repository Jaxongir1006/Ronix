from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields,TranslatableModel

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))
    
    def __str__(self):
        return self.question
    
class NewsletterSubscriber(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Full name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Subscribed at"))

    def __str__(self):
        return self.email
    
class AboutUs(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=255, verbose_name=_("Title")),
        subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Subtitle")),
        content = models.TextField(verbose_name=_("Main content"))
    )
    image = models.ImageField(upload_to='aboutus/', blank=True, null=True, verbose_name=_("Main image"))
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"
    
    @property
    def imageURL(self):
        if self.image:
            return self.imageURL
        else:
            return ''
    