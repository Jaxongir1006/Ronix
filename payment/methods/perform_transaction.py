from rest_framework.response import Response
from models import Payment
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class PerformTransaction:
    def __call__(self, params: dict):
        data = params.get('params', {})
        transaction_id = data.get('id')

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

        if transaction.state != 1:
            if transaction.state == 2:
                return Response({
                    'state': transaction.state,
                    'perform_time': transaction.perform_time,
                    'transaction': transaction.transaction_id
                })
            else:
                return Response({
                    "error": {
                        "code": -31008,
                        "message": {
                            "uz": _("Tranzaksiyani bajarib bolmaydi."),
                            "ru": _("Невозможно выполнить транзакцию."),
                            "en": _("Unable to perform the transaction.")
                        }
                    },
                    "id": params.get("id")
                })

        transaction.state = 2
        transaction.perform_time = now()
        transaction.save()

        return Response({
            'state': transaction.state,
            'perform_time': transaction.perform_time,
            'transaction': transaction.transaction_id
        })
        
