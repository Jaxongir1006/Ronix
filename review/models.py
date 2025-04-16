from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields,TranslatableModel

class Review(models.Model):
    product = models.ForeignKey(verbose_name = _("product"), to='products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name = _("user"), to='users.User', on_delete=models.CASCADE)
    rate = models.IntegerField(verbose_name= _("rate"))
    comment = models.TextField(verbose_name=_('Comment'))

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


class AboutContent(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        description = models.TextField()
    )

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"
  
class CountryContent(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class InfoContent(models.Model):
    city = models.CharField(max_length=300)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)    
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.city