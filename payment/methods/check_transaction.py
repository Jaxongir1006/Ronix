from rest_framework.response import Response
from payment.models import Payment
import time
from django.utils.translation import gettext_lazy as _

class CheckTransaction:
    def __call__(self, params: dict):
        data = params.get('params', {})
        transaction_id = data.get('id')

        try:
            transaction = Payment.objects.get(transaction_id = transaction_id)
            
            return Response({
                "result": {
                    "create_time": int(transaction.created_at_ms) if transaction.created_at_ms else int(time.time() * 1000),
                    "perform_time": int(transaction.perform_time) if transaction.perform_time else 0,
                    "cancel_time": int(transaction.cancel_time) if transaction.cancel_time else 0,
                    "transaction": transaction.transaction_id,
                    "state": transaction.state or 1,
                    "reason": int(transaction.reason) if transaction.reason and transaction.reason.isdigit() else None
                },
                "error": None,
                "id": params.data.get("id")
            })
            
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