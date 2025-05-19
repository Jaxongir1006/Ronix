from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .methods.check_transaction import CheckTransaction
from .methods.cancel_transaction import CancelTransaction
from .methods.create_transaction import CreateTransaction
from .methods.perform_transaction import PerformTransaction
from .methods.check_perform_transaction import CheckPerformTransaction      
from .methods.get_statement import GetStatement
from .methods.generate_link import GeneratePayLink
from rest_framework.decorators import action
from decimal import Decimal

class PaymeViewSet(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        method = request.data.get("method")
        params = request.data.get("params", {})

        handler_map = {
            "CheckPerformTransaction": CheckPerformTransaction(),
            "CreateTransaction": CreateTransaction(),
            "PerformTransaction": PerformTransaction(),
            "CancelTransaction": CancelTransaction(),
            "GetStatement": GetStatement(),
            "CheckTransaction": CheckTransaction()
        }

        handler = handler_map.get(method)
        if handler is None:
            return Response({
                "error": {
                    "code": -32601,
                    "message": {
                        "uz": "Metod topilmadi",
                        "ru": "Метод не найден",
                        "en": "Method not found"
                    }
                }
            })

        return handler(params)

    @action(detail=False, methods=["post"], url_path="generate-link")
    def generate_pay_link(self, request):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")

        if not order_id or not amount:
            return Response({
                "error": "order_id va amount bolishi kerak"
            }, status=400)

        try:
            amount = Decimal(amount)
        except:
            return Response({
                "error": "Notogri amount format"
            }, status=400)

        pay_link = GeneratePayLink(id=order_id, amount=amount).generate_link()
        return Response({
            "pay_link": pay_link
        })