from models import Payment

class GetStatement:
    def __call__(self, params: dict) -> dict:
        """
        Handles the getStatement request from Payme.
        """
        from_timestamp = params.get("from")
        to_timestamp = params.get("to")

        if from_timestamp is None or to_timestamp is None:
            return {"error": "Missing parameters"}

        payments = Payment.objects.filter(
            created_at_ms__gte=from_timestamp,
            created_at_ms__lte=to_timestamp,
            state__in=[1, 2]
        ).order_by("created_at_ms")

        transactions = []
        for payment in payments:
            transactions.append({
                "id": payment.id,
                "time": payment.time,
                "amount": int(payment.amount * 100),
                "account": {
                    "login": str(payment.user.id)       
                },
                "create_time": int(payment.created_at_ms),
                "perform_time": payment.perform_time if payment.perform_time else 0,
                "cancel_time": payment.cancel_time if payment.cancel_time else 0,
                "transaction": payment.transaction_id,
                "state": payment.state,
                "reason": payment.reason if payment.reason else None
            })

        response: dict = {
            "result": {
                "transactions": transactions
            }
        }
        return response