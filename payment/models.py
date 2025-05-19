from django.db import models

class Payment(models.Model):
    class PaymentOperators(models.TextChoices):
        CLICK = 'Click', 'Click'
        PAYME = 'PAYME', 'PayMe'

    class PaymentStatus(models.TextChoices):
        WAITING = "waiting", "Kutmoqda"
        PREAUTH = "preauth", "Oldindan tasdiqlash"
        CONFIRMED = "confirmed", "Tasdiqlandi"
        REJECTED = "rejected", "Rad etildi"
        REFUNDED = "refunded", "Qaytarildi"
        ERROR = "error", "Xato"
        INPUT = "input", "Kiritish"

    state = models.IntegerField(
        choices=[
            (-2, "Xatolik (Payme)"),
            (-1, "Bekor qilingan (Payme)"),
            (1, "Yaratilgan (Payme)"),
            (2, "Tasdiqlangan (Payme)")
        ],
        null=True,
        blank=True,
        verbose_name="Tranzaksiya holati (Payme)"
    )
    transaction_id = models.CharField(max_length=255, null=True, blank=False, verbose_name="Tranzaksiya ID")
    user = models.ForeignKey(to='users.User',on_delete=models.CASCADE,blank=True, null=True)
    amount = models.FloatField(null=True, blank=True, verbose_name="Miqdor")
    time = models.BigIntegerField(null=True, blank=True, verbose_name="Vaqt")
    perform_time = models.BigIntegerField(null=True, default=0, verbose_name="Bajarilgan vaqti")
    cancel_time = models.BigIntegerField(null=True, default=0, verbose_name="Bekor qilingan vaqti")
    status = models.CharField(max_length=30, null=True, choices=PaymentStatus.choices, verbose_name="Holati") # subscibe api uchun
    reason = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sabab")
    created_at_ms = models.CharField(max_length=255, null=True, blank=True, verbose_name="Yaratilgan vaqti (ms)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")
    payment_operator = models.CharField(max_length=30, choices=PaymentOperators.choices, null=True, blank=True, verbose_name="To'lov operatori", default=PaymentOperators.PAYME)


    class Meta:
        verbose_name = "To'lov "
        verbose_name_plural = "To'lovlar "

    def __str__(self):
        return str(self._id)

class PeymentVerification(models.Model):
    client = models.ForeignKey(to='users.User',on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.time}"