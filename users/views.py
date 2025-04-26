from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializer import RegisterLoginSerializer, VerifyCodeSerializer
from .models import User
from core.utils import generate_verification_code, send_email_code

class RegisterLoginView(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')

        # Random 6 digit code
        code = generate_verification_code()
        user.verification_code = code
        user.save()

        if email:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email}
            )
            send_email_code(email, code)
        elif phone_number:
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={'username': phone_number}
            )


        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)


class VerifyCodeView(viewsets.ViewSet):
    def create(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')

        try:
            if phone_number:
                user = User.objects.get(phone_number=phone_number)
            else:
                user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code != code:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.verification_code = None  # Kodni ochirib tashlaymiz
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)
