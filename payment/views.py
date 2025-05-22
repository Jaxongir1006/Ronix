from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from decimal import Decimal
from .methods.generate_click_link import GenerateClickLink
from django.views.decorators.csrf import csrf_exempt
from .utils import click_utils
from django.utils.decorators import method_decorator

class PaymeCallbackAPIView(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        # Bu yerda istasangiz frontendga qaytarishingiz mumkin yoki API response berishingiz mumkin
        return Response({"message": "To'lov muvaffaqiyatli yakunlandi"})


class ClickPaymentViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='generate-link')
    def generate_link(self, request):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")

        if not order_id or not amount:
            return Response({"error": "order_id va amount talab qilinadi"}, status=400)

        try:
            amount = Decimal(amount)
        except:
            return Response({"error": "amount notogri formatda"}, status=400)

        payment_link = GenerateClickLink(order_id=order_id, amount=amount).generate_link()
        return Response({"payment_link": payment_link})

@method_decorator(csrf_exempt, name='dispatch')
class ClickTransactionViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='prepare')
    def prepare(self, request):
        return click_utils.prepare(request)

    @action(detail=False, methods=['post'], url_path='complete')
    def complete(self, request):
        return click_utils.complete(request)