from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from rest_framework.exceptions import ValidationError
from parler.managers import TranslatableManager


class Category(TranslatableModel):

    translations = TranslatedFields(
        name = models.CharField(max_length=200, verbose_name = _('Name'),blank=True,null=True),
        description = models.TextField(verbose_name = _('Description'),blank=True,null=True)
    )

    image = models.ImageField(upload_to='category/', verbose_name = _('Image'))

    objects = TranslatableManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed Category"

    @property
    def imageURL(self):
        return self.image.url if self.image else ''

class SubCategory(TranslatableModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name=_('Category'))

    translation = TranslatedFields(
        name = models.CharField(max_length=200, verbose_name=_('Name')),
        description = models.TextField(verbose_name=_("Description"))
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_("Parent SubCategory")
    )

    image = models.ImageField(upload_to='subcategory/', verbose_name=_("Image"), blank=True, null=True)

    objects = TranslatableManager()

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed SubCategory"

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, verbose_name = _('Name')),
        features = models.TextField(verbose_name = _('Features')),
        description = models.TextField(verbose_name = _('Description')),
        made_in = models.CharField(max_length=200, verbose_name = _('Made in'), blank=True, null=True),
    )
    barcode_color = models.CharField(max_length=200, verbose_name=_('Barcode for Color Box'), blank=True, null=True)
    barcode_carton = models.CharField(max_length=200, verbose_name=_('Barcode for Inner Carton'),blank=True,null=True)
    image = models.ImageField(upload_to='products/', verbose_name = _('Image'))
    model = models.CharField(max_length=100, verbose_name = _('Model'))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', verbose_name = _('Category'))
    price = models.FloatField(verbose_name=_('Price'), blank=True, null=True)

    objects = TranslatableManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed Product"

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
class Specification(TranslatableModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name=_('Product'), null=True, blank=True)
    translations = TranslatedFields(
        type = models.CharField(max_length=100, verbose_name = _('Type')),
        size = models.CharField(max_length=100, verbose_name = _('Size')),
        power = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Power')),
        voltage = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Voltage')),
        frequency = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Frequency')),
        speed = models.CharField(max_length=100, verbose_name = _('Speed')),
        capacity_wood = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Capacity in wood')),
        capacity_steel = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Capacity in steel')),
        weight = models.CharField(max_length=100, verbose_name = _('Weight')),
        supplied_in = models.CharField(max_length=100, verbose_name = _('Supplied in'))
    )

    objects = TranslatableManager()

    class Meta: 
        verbose_name = _("Specification")
        verbose_name_plural = _('Specifications')

    def __str__(self):
        return self.safe_translation_getter('type', any_language=True) or 'Unnamed Specification'

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('product'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Image'), blank=True, null=True)
    video = models.FileField(upload_to='videos/',verbose_name=_('Video'), blank=True,null=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"{self.product} - Image/Video"


    def clean(self):
        if not self.image and not self.video:
            raise ValidationError(_('At least one of image or video must be provided.'))   
    
    @property
    def media_url(self):
        return self.image.url if self.image else (self.video.url if self.video else "")
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
    
class ProductDetail(TranslatableModel):
    
    main_image = models.ImageField(upload_to='products/', verbose_name=_('Main image'), blank=True, null=True)

    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('Title'), blank=True, null=True),
        description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='details', blank=True, null=True)

    objects = TranslatableManager()

    @property
    def imageURL(self):
        return self.main_image.url if self.main_image else ''
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or 'Unnamed title'
    
    class Meta:
        verbose_name = _("Product Detail")
        verbose_name_plural = _("Product Details")