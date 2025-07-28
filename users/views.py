from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny

class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                "message": "User registered successfully",
                "access_token": data['access_token'],
                "refresh_token": data['refresh_token']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Login successful",
                "access_token": serializer.validated_data["access_token"],
                "refresh_token": serializer.validated_data["refresh_token"],
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
