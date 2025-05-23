from django.db import models
from django.utils.translation import gettext_lazy as _ 
from parler.models import TranslatableManager
class Order(models.Model):
    class StatusEnum(models.TextChoices):
        PENDING = 'pending', _('Pending')                # Buyurtma yaratilgan, hali ko‘rilmagan
        PAID = 'paid', _('Paid')                         # Tolov qilingan
        CANCELED = 'canceled', _('Canceled')             # Buyurtma bekor qilingan
        AWAITING_PAYMENT = 'awaiting payment', _('Awaiting Payment') # tolov qilinishi kutilmoqda

    status=models.CharField(verbose_name = _("order_status"),max_length=30,choices=StatusEnum.choices, default=StatusEnum.PENDING)
    user=models.ForeignKey(verbose_name=_("user") ,to='users.User',on_delete=models.CASCADE)
    total_price = models.FloatField(verbose_name=_('Total price'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    objects = TranslatableManager()

    class Meta:
        verbose_name=_("Order")
        verbose_name_plural=_("Orders")

    class Meta:
        ordering = ['-id']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

class OrderItem(models.Model):
    order=models.ForeignKey(verbose_name=_("order"), to =Order,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(verbose_name=_("product") ,to = 'products.Product',on_delete=models.CASCADE)
    quantity=models.IntegerField(verbose_name= _("quantity"))
    price = models.FloatField(verbose_name=_('Price'), blank=True, null=True)

    class Meta:
        verbose_name=_("Order Item")
        verbose_name_plural=_("Order Items")