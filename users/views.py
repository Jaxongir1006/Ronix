from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterSerializer, VerifyCodeSerializer,UserSerializer,UserProfileSerializer,LoginSerializer
from .serializer import SendResetCodeSerializer,ConfirmResetPasswordSerializer,AddressSerializer
from .models import User,UserProfile,Address
import requests
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action
from cart.models import Cart


class RegisterView(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Royxatdan otish muvaffaqiyatli!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(viewsets.ViewSet):
    def create(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        session_id = request.data.get("session_id")
        
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

        if session_id:
            try:
                cart = Cart.objects.get(session_id=session_id, user__isnull=True)
                cart.user = user
                cart.session_id = None  # optional: uni tozalab qo'yish ham mumkin
                cart.save()
            except Cart.DoesNotExist:
                pass


        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Successfully logged in!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Couldn't log in"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='send-code')
    def send_code(self, request):
        serializer = SendResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Kod yuborildi!"})

    @action(detail=False, methods=['post'], url_path='confirm')
    def confirm_reset(self, request):
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Parol muvaffaqiyatli ozgartirildi!"})



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


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'], url_path='me')
    def me(self, request):
        try:
            profile = request.user.profile  # OneToOneField orqali
        except UserProfile.DoesNotExist:
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(profile, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            profile.delete()
            return Response({'detail': 'User profile deleted.'}, status=status.HTTP_204_NO_CONTENT)


class AddressViewSet(viewsets.ModelViewSet):
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