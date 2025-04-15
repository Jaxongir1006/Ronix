from django.db import models
from django.utils.translation import gettext_lazy as _


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