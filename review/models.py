from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields,TranslatableModel

class Review(models.Model):
    product = models.ForeignKey(verbose_name = _("product"), to='products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name = _("user"), to='users.User', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name=_('Comment'))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

class Rate(models.Model):
    power_and_quality=models.PositiveSmallIntegerField(default=0, verbose_name=_('Power And Quality')),
    easy_to_use=models.PositiveSmallIntegerField(default=0, verbose_name=_('Easy To Use')),
    safety=models.PositiveSmallIntegerField(default=0, verbose_name=_('Safety')),
    ergonomy=models.PositiveSmallIntegerField(default=0, verbose_name=_('Ergonomy')),
    cost=models.PositiveSmallIntegerField(default=0, verbose_name=_('Cost')),
    review = models.OneToOneField(Review, on_delete=models.CASCADE)

    def average_rating(self):
        return round((
            self.power_and_quality +
            self.easy_to_use +
            self.safety +
            self.ergonomy +
            self.cost
        ) / 5, 2)

    def __str__(self):
        return f"Rating for review #{self.review.id}"

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



# class AboutContent(TranslatableModel):
#     translations = TranslatedFields(
#         title = models.CharField(max_length=200),
#         description = models.TextField()
#     )

#     def __str__(self):
#         return self.safe_translation_getter('title', any_language=True) or "Unnamed title"
  
# class CountryContent(models.Model):
#     name = models.CharField(max_length=200)
    
#     def __str__(self):
#         return self.name


# class InfoContent(models.Model):
#     city = models.CharField(max_length=200)
#     address = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)    
#     phone = models.CharField(max_length=15)
    
#     def __str__(self):
#         return self.city
    