from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CartManager

class Cart(models.Model):
    user = models.ForeignKey(verbose_name=_("Cart_user"), to='users.User', null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    custom = CartManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_cart_per_user'),
            models.UniqueConstraint(fields=['session_id'], name='unique_cart_per_session'),
        ]
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

class CartItem(models.Model):
    cart = models.ForeignKey(verbose_name=_("Cart"),to=Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(verbose_name=_("Product"), to="products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')