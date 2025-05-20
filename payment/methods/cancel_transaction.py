from rest_framework.response import Response
from models import Payment
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class CancelTransaction:
    def __call__(self, params: dict):
        data = params.get('params', {})
        transaction_id = data.get('id')
        reason = data.get('reason')

        try:
            transaction = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response({
                "error": {
                    "code": -31003,
                    "message": {
                        "uz": _("Tranzaksiya topilmadi."),
                        "ru": _("Транзакция не найдена."),
                        "en": _("Transaction not found.")
                    }
                },
                "id": params.get("id")
            })

        # 1. Tranzaksiya hali bajarilmagan (state=1)
        if transaction.state == 1:
            transaction.state = -1
            transaction.reason = reason
            transaction.cancel_time = now()
            transaction.save()

        # 2. Tranzaksiya bajarilgan bo‘lsa ham, faqat status o‘zgaradi
        elif transaction.state == 2:
            transaction.state = -2
            transaction.reason = reason
            transaction.cancel_time = now()
            transaction.save()

        return Response({
            'state': transaction.state,
            'cancel_time': transaction.cancel_time,
            'transaction': transaction.transaction_id
        })

        