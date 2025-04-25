import requests
from django.core.mail import send_mail
from random import randint

def send_sms(phone_number, message):
    token = "ESKIZ_TOKEN_HERE"
    url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "mobile_phone": phone_number,
        "message": message,
        "from": "4546"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def generate_verification_code():
    return str(randint(100000, 999999))

def send_email_code(to_email, code):
    subject = "Tasdiqlash kodingiz"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    send_mail(subject, message, 'jahongir192006@example.com', [to_email])