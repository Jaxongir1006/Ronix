from django.http import JsonResponse
from django.conf import settings
from payment.models import Payment
import hashlib
from uuid import uuid4
from order.models import Order

PaymentStatus = Payment.PaymentStatus

def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True

def order_load(order_id):
    if len(order_id)>6:
        return None
    try:
        return Order.objects.get(id = int(order_id))
    except Order.DoesNotExist:
        return None

def payment_load(paymet_id):
    if len(paymet_id)>100000000:
        return None
    try:
        return Payment.objects.get(id = int(paymet_id))
    except:
        return None
    
def click_secret_key():
    secret_key = settings.CLICK['secret_key']
    return secret_key


def click_webhook_errors(request):
    click_trans_id = request.POST.get('click_trans_id', None)
    service_id = request.POST.get('service_id', None)
    click_paydoc_id = request.POST.get('click_paydoc_id', None)
    order_id = request.POST.get('merchant_trans_id', None)
    amount = request.POST.get('amount', None)
    action = request.POST.get('action', None)
    error = request.POST.get('error', None)
    error_note = request.POST.get('error_note', None)
    sign_time = request.POST.get('sign_time', None)
    sign_string = request.POST.get('sign_string', None)
    merchant_prepare_id = request.POST.get('merchant_prepare_id', None) if action != None and action == '1' else ''
    if isset(request.POST,
             ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note', 'sign_time',
              'sign_string']) or (
            action == '1' and isset(request.POST, ['merchant_prepare_id'])):
        return {
            'error': '-8',
            'error_note': 'Error in request from click'
        }

    signString = '{}{}{}{}{}{}{}{}'.format(
        click_trans_id, service_id, click_secret_key(), order_id, merchant_prepare_id, amount, action, sign_time
    )
    encoder = hashlib.md5(signString.encode('utf-8'))
    signString = encoder.hexdigest()
    if signString != sign_string:
        return {
            'error': '-1',
            'error_note': 'SIGN CHECK FAILED!'
        }

    if action not in ['0', '1']:
        return {
            'error': '-3',
            'error_note': 'Action not found'
        }

    order = order_load(order_id)
    if not order:
        return {
            'error': '-5',
            'error_note': 'User does not exist'
        }
    
    if float(amount) < 500 or float(amount) > 100000000:
        return {
            'error': '-2',
            'error_note': 'Incorrect parameter amount'
        }

    payment = payment_load(merchant_prepare_id) if merchant_prepare_id else None
    if payment:
        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

    if action == '1':
        if not payment_load(merchant_prepare_id):
            return {
                'error': '-6',
                'error_note': 'Transaction not found'
            }

    if payment:
        if payment.status == PaymentStatus.REJECTED:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }

    if  int(error) == -5017:
        return {
            'error': '-9',
            'error_note': 'Transaction cancelled'
        }

    return {
        'error': '0',
        'error_note': 'Success'
    }


def prepare(request):
    if request.method == "POST":
        result = click_webhook_errors(request)
        order_id = request.POST.get('merchant_trans_id', None)
        order = order_load(order_id)
        if order:
            payment, created = Payment.objects.get_or_create(order=order_id,amount = float(request.POST.get('amount')),status = PaymentStatus.WAITING)
        else:
            payment = None
        result['click_trans_id'] = request.POST.get('click_trans_id', None)
        result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = payment.id if payment else 0
        result['merchant_confirm_id'] = request.POST.get('merchant_trans_id', None)
        return JsonResponse(result)
    else:
        return JsonResponse({'bumm':'bumm'})

def complete(request):
    result = click_webhook_errors(request)
    print(result)
    order_id = request.POST.get('merchant_trans_id', None)
    payment_id = request.POST.get('merchant_prepare_id', None)
    order = order_load(order_id) if payment_id else None
    payment = payment_load(payment_id)
    if request.POST.get('error', None) != None and int(request.POST.get('error', None)) < 0:
        payment.status = PaymentStatus.REJECTED
        payment.save()
    if result['error'] == '0':
        payment.status = PaymentStatus.CONFIRMED
        payment.save()
        order.status = Order.StatusEnum.PAID
        order.save()
    if payment:
        if int(result['error']) < 0:
            if int(result['error']) == -9:
                payment.status = PaymentStatus.REJECTED
            else:
                payment.status = PaymentStatus.ERROR
            payment.save()
    result['click_trans_id'] = request.POST.get('click_trans_id', None)
    result['merchant_trans_id'] = request.POST.get('merchant_trans_id', None)
    result['merchant_prepare_id'] = request.POST.get('merchant_prepare_id', None)
    result['merchant_confirm_id'] = request.POST.get('merchant_prepare_id', None)
    return JsonResponse(result)