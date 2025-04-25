from rest_framework.viewsets import ViewSet
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class UserViewset(ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        if request.user.is_authenticated:
            return Response({"message": "You are already logged in."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    