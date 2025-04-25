from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import PhoneNumberSerializer,EmailSerializer
from .utils import send_sms,send_email_code,generate_verification_code

class SendSMSView(ViewSet):

    def create(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            message = "Sizning tasdiqlash kodingiz: 12345"
            result = send_sms(phone, message)
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SendVerificationEmailView(ViewSet):
    
    def create(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = generate_verification_code()
            send_email_code(email, code)
            return Response({'message': 'Tasdiqlash kodi emailga yuborildi', 'email': email})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)