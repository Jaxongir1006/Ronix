from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
class Card(models.Model):
    card_number = models.CharField(max_length=16, unique=True, verbose_name=_("Card Number"))
    cardholder_name = models.CharField(max_length=100, verbose_name=_("Cardholder Name"))
    expiration_date = models.DateField(verbose_name=_("Expiration date"))
    cvv = models.CharField(max_length=4, verbose_name="CVV")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cards', verbose_name=_("User"))

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return f"{self.cardholder_name} - {self.card_number}"
    
    def clean(self):
        # Card number must be all digits and 16 characters
        if not self.card_number.isdigit() or len(self.card_number) != 16:
            raise ValidationError(_("Card number must be 16 digits."))

        # CVV must be 3 or 4 digits
        if not self.cvv.isdigit() or len(self.cvv) not in [3, 4]:
            raise ValidationError(_("CVV must be 3 or 4 digits."))

    