from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from order.models import Order
from urllib.parse import urlencode

# sozlamalar
PAYME_MERCHANT_ID = 'YOUR_MERCHANT_ID'
PAYME_URL = 'https://checkout.paycom.uz'
CALLBACK_URL = 'https://ronixtools.uz/payment/payme/callback/'


class PaymeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='initiate')
    def payme_initiate(self, request):
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status == 'paid':
                return Response({'detail': 'Order already paid'}, status=status.HTTP_400_BAD_REQUEST)

            amount_in_tiyin = int(order.amount * 100)

            payment_data = {
                "merchant": PAYME_MERCHANT_ID,
                "amount": amount_in_tiyin,
                "account": {
                    "order_id": order.external_id
                },
                "callback": CALLBACK_URL
            }

            return Response({
                "payme_url": PAYME_URL,
                "payment_data": payment_data
            })

        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)



CLICK_MERCHANT_ID = 'YOUR_CLICK_MERCHANT_ID'
CLICK_SERVICE_ID = 'YOUR_CLICK_SERVICE_ID'
CLICK_SECRET_KEY = 'YOUR_CLICK_SECRET_KEY'
CLICK_PAYMENT_URL = 'https://my.click.uz/services/pay'

class ClickViewSet(ViewSet):

    @action(detail=False, methods=['post'], url_path='initiate', permission_classes = [IsAuthenticated])
    def click_initiate(self, request):
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.status == 'paid':
                return Response({'detail': 'Order already paid'}, status=status.HTTP_400_BAD_REQUEST)

            amount = float(order.amount)

            params = {
                'service_id': CLICK_SERVICE_ID,
                'merchant_id': CLICK_MERCHANT_ID,
                'amount': amount,
                'transaction_param': order.external_id,
                'return_url': 'https://ronixtools.uz/payment-success/',
                'cancel_url': 'https://ronixtools.uz/payment-cancel/',
            }

            click_url = f"{CLICK_PAYMENT_URL}?{urlencode(params)}"
            return Response({'click_url': click_url})

        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='callback', permission_classes=[AllowAny])
    def click_callback(self, request):
        data = request.data

        external_id = data.get('merchant_trans_id')
        sign_string = f"{external_id}{data.get('amount')}{CLICK_SECRET_KEY}"
        received_sign = data.get('sign_time')

        try:
            order = Order.objects.get(external_id=external_id)

            # Imzo tekshirish shart, Click hujjatiga qarab sozlashing mumkin
            if received_sign != sign_string:  # Bu faqat misol!
                return Response({'error': 'Invalid signature'}, status=status.HTTP_403_FORBIDDEN)

            order.status = 'paid'
            order.save()

            return Response({'success': True})

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
