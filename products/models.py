from django.db import models
from django.utils.translation import gettext_lazy as _


class Specification(models.Model):
    type = models.CharField(max_length=100, verbose_name = _('Type'))
    size = models.CharField(max_length=100, verbose_name = _('Size'))
    power = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Power'))
    voltage = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Voltage'))
    frequency = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Frequency'))
    speed = models.CharField(max_length=100, verbose_name = _('Speed'))
    capacity_wood = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Capacity in wood'))
    capacity_steel = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Capacity in steel'))
    weight = models.CharField(max_length=100, verbose_name = _('Weight'))
    supplied_in = models.CharField(max_length=100, verbose_name = _('Supplied in'))

    def __str__(self):
        return f'{self.type}'

class Category(models.Model):
    image = models.ImageField(upload_to='category/', verbose_name = _('Image'))
    name = models.CharField(max_length=200, verbose_name = _('Name'))
    description = models.TextField(verbose_name = _('Description'))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name = _('Image'))
    name = models.CharField(max_length=200, verbose_name = _('Name'))
    model = models.CharField(max_length=100, verbose_name = _('Model'))
    features = models.TextField(verbose_name = _('Features'))
    description = models.TextField(verbose_name = _('Description'))
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name='products', verbose_name = _('Specification'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name = _('Category'))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    def __str__(self):
        return f'{self.name}'
