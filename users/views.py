from rest_framework.viewsets import ModelViewSet,ViewSet
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status

class UserViewset(ViewSet):
    def create(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

