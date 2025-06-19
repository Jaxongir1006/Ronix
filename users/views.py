from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializer import RegisterSerializer,LoginSerializer,VerifyCodeSerializer,AddressSerializer,UserSerializer,ResendCodeSerializer
from .serializer import ChangePasswordSerializer,ChangePasswordWithEmailSerializer,VerifyCodeChangePasswordSerializer, UserProfileSerializer,UserEmailVerifySerializer
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Address,User
from rest_framework_simplejwt.tokens import RefreshToken
import requests

class RegisterViewSet(ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response({"message": _(f"Verification code has been sent to {user_data['email']}")}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='verify')
    def verify_code(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": _("User verified successfully"),
                "access_token": serializer.validated_data['access_token'],
                "refresh_token": serializer.validated_data['refresh_token'],
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='resend-code')
    def resend_code(self, request):
        serializer = ResendCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": _(f"Verification code resent to {serializer.validated_data['email']}")},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginViewSet(ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": _("Login successful"),
                "access_token": serializer.validated_data["access_token"],
                "refresh_token": serializer.validated_data["refresh_token"],
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordViewSet(ViewSet):
    @action(detail=False, methods=['post'], url_path='with-password')
    def with_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Password changed successfully")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],url_path='with-email')
    def find_email(self, request):
        serializer = ChangePasswordWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": _("Verification code has been sent to your email")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_code(self, request):
        serializer = VerifyCodeChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": _("Password changed successfully")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'], url_path='me')
    def me(self, request):
        user = self.get_object()

        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            serializer = UserProfileSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response({'detail': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
        
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_email(self, request):
        serializer = UserEmailVerifySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({"message": _("Email verified successfully")}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

class GoogleAuthViewSet(ViewSet):
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
            user.save()

        # JWT token yaratamiz
        refresh = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)