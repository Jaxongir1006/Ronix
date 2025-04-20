from .serializer import ContactUsSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

class ContactUsViewSet(ViewSet):    
    def create(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact request submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)