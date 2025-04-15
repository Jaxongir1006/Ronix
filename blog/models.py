from django.db import models
from django.utils.translation import gettext_lazy as _

class Blog(models.Model):
    image = models.ImageField(upload_to='blog/', verbose_name=_('Image'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description '))
    views = models.IntegerField(default=0, verbose_name=_('View'))
    created_time = models.DateTimeField(auto_now_add=True,verbose_name=_('Created time')) 
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated time'))

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

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
