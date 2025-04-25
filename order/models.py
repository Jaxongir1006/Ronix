from django.db import models
from django.utils.translation import gettext_lazy as _ 
from parler.models import TranslatableManager

class Order(models.Model):
    class StatusEnum(models.TextChoices):
        PACKAGING='packaging', _('Packaging')
        SHIPPED='shipped', _('Shipped')
        CANCELED='canceled', _('Canceled')
        AWAITING_PICKUP='awaiting pickup', _('Awaiting pickup')
        COMPLETED='completed', _('Completed')

    status=models.CharField(verbose_name = _("order_status"),max_length=30,choices=StatusEnum.choices)
    user=models.ForeignKey(verbose_name=_("user") ,to='users.User',on_delete=models.CASCADE)
    
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
    discount=models.FloatField(verbose_name = _("discount"), blank=True,null=True)

    class Meta:
        verbose_name=_("Order Item")
        verbose_name_plural=_("Order Items")