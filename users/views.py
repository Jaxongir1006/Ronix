from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterLoginSerializer, VerifyCodeSerializer,UserSerializer
from .models import User
from core.utils import generate_verification_code, send_email_code,send_sms
import requests
from rest_framework.permissions import AllowAny

class RegisterLoginView(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')

        # Random 6   code
        code = generate_verification_code()

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
            send_sms(phone_number, code)
        else:
            return Response({"error": "Phone number or email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user.verification_code = code
        user.save()

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
        user.verification_code = None
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class GoogleAuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        token = request.data.get('token')

        if not token:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Googledan user ma'lumotlarini olish
        try:
            response = requests.get(
                f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}'
            )
            user_info = response.json()
        except Exception as e:
            return Response({'error': 'Failed to fetch user info from Google.'}, status=status.HTTP_400_BAD_REQUEST)

        email = user_info.get('email')
        username = user_info.get('name')

        if not email:
            return Response({'error': 'Email not found in Google account.'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = username
            user.is_verified = True
            user.save()

        # JWT token yaratamiz
        refresh = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)