from rest_framework.response import Response
from models import Payment
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
from order.models import Order
from utils.services import check_perform_transaction

class CreateTransaction:
    def __call__(self, params: dict):
        data = params.get('params', {})
        transaction_id = data.get('id')
        amount = data.get('amount')
        account = data.get('account', {})

        try:
            transaction = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            perform_result = check_perform_transaction(amount, account)
            if not perform_result["success"]:
                return Response(perform_result["error"])

            transaction = Payment.objects.create(
                transaction_id=transaction_id,
                amount=amount,
                state=1,
                created_at=now(),
                order_id=account.get('order')
            )

            # Buyurtmani "to‘lov kutilmoqda" holatiga o‘tkazish (agar kerak bo‘lsa)
            Order.objects.filter(id=account.get("order")).update(status="awaiting_payment")

            return Response({
                "transaction": transaction.transaction_id,
                "create_time": transaction.created_at,
                "state": transaction.state
            })

        if transaction.state == 1:
            timeout_limit = timedelta(minutes=12)
            if now() - transaction.created_at > timeout_limit:
                transaction.state = -1
                transaction.reason = 4
                transaction.cancel_time = now()
                transaction.save()

                return Response({
                    "error": {
                        "code": -31008,
                        "message": {
                            "uz": _("Tranzaksiya muddati tugagan."),
                            "ru": _("Время транзакции истекло."),
                            "en": _("Transaction timeout.")
                        }
                    },
                    "state": transaction.state,
                    "transaction": transaction.transaction_id,
                    "create_time": transaction.created_at
                })


            return Response({
                "transaction": transaction.transaction_id,
                "create_time": transaction.created_at,
                "state": transaction.state
            })


        return Response({
            "error": {
                "code": -31008,
                "message": {
                    "uz": _("Tranzaksiyani yaratib bolmaydi."),
                    "ru": _("Невозможно создать транзакцию."),
                    "en": _("Cannot create transaction.")
                }
            },
            "id": params.get("id")
        })