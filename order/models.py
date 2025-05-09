from django.db import models
from django.utils.translation import gettext_lazy as _ 
from parler.models import TranslatableManager
class Order(models.Model):
    class StatusEnum(models.TextChoices):
        PENDING = 'pending', _('Pending')                # Buyurtma yaratilgan, hali ko‘rilmagan
        VERIFIED = 'verified', _('Verified')             # To‘lov yoki foydalanuvchi tasdiqlangan
        PACKAGING = 'packaging', _('Packaging')          # Buyurtma yig‘ilmoqda
        SHIPPED = 'shipped', _('Shipped')                # Yetkazib berishga yuborilgan
        COMPLETED = 'completed', _('Completed')          # Yetkazildi, yakunlandi
        CANCELED = 'canceled', _('Canceled')             # Buyurtma bekor qilingan


    status=models.CharField(verbose_name = _("order_status"),max_length=30,choices=StatusEnum.choices, default=StatusEnum.PENDING)
    user=models.ForeignKey(verbose_name=_("user") ,to='users.User',on_delete=models.CASCADE)
    total_price = models.FloatField(verbose_name=_('Total price'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = TranslatableManager()

    class Meta:
        verbose_name=_("Order")
        verbose_name_plural=_("Orders")

    class Meta:
        ordering = ['-id']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

class OrderItem(models.Model):
    order=models.ForeignKey(verbose_name=_("order"), to =Order,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(verbose_name=_("product") ,to = 'products.Product',on_delete=models.CASCADE)
    quantity=models.IntegerField(verbose_name= _("quantity"))
    price = models.FloatField(verbose_name=_('Price'), blank=True, null=True)

    class Meta:
        verbose_name=_("Order Item")
        verbose_name_plural=_("Order Items")