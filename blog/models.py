from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel,TranslatedFields

class Blog(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Description '))
    )
    image = models.ImageField(upload_to='blog/', verbose_name=_('Image'))
    views = models.IntegerField(default=0, verbose_name=_('View'))
    created_time = models.DateTimeField(auto_now_add=True,verbose_name=_('Created time')) 
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated time'))
    rate = models.IntegerField(verbose_name= _("rate"))

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed title"

class BlogContent(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title')),
        description = models.TextField(verbose_name=_('Description'))
    )

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or "Unnamed titlej"

class BlogImages(TranslatableModel):
    translations = TranslatedFields(
        description = models.TextField(verbose_name=_('Description')),
    )
    image = models.ImageField(upload_to='blog/', verbose_name=_('Image'))

    @property
    def ImageURL(self):
        if self.image:
            return self.image.url
        return ''

class Comment(models.Model):
    text = models.TextField(verbose_name=_('Text'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created time'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Blog'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return self.name
